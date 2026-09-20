import uuid
import asyncio
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.integrations.mqtt_client import (
    get_iot_provider,
    IoTProvider,
    MQTTTopicBuilder,
    SensorTelemetryPayload
)
from app.integrations.mock_iot import mock_iot_service
from app.integrations.websocket_manager import ws_manager
from app.models.sensor import SensorReading, SensorNode
from app.models.task import FarmTask
from app.models.audit import ActivityLog
from app.utils.logger import logger

class IoTService:
    def __init__(self):
        self.provider: IoTProvider = get_iot_provider()
        self.valve_states: Dict[str, str] = {
            "fieldA": "Closed",
            "fieldB": "Closed",
            "fieldC": "Closed"
        }
        self.active_valve_tasks: Dict[str, asyncio.Task] = {}

    async def process_sensor_payload(
        self,
        farm_id: str,
        field_id: str,
        sensor_id: str,
        payload_data: Dict[str, Any],
        db: Optional[AsyncSession] = None
    ) -> Dict[str, Any]:
        """Validate, store, and route incoming IoT sensor telemetry."""
        # 1. Validate payload with strict schema
        payload = SensorTelemetryPayload(**payload_data)

        # 2. Update in-memory telemetry state for immediate real-time reads
        mock_iot_service.telemetry["soilMoisture"] = payload.soil_moisture
        mock_iot_service.telemetry["soilTemperature"] = payload.temperature
        mock_iot_service.telemetry["airHumidity"] = payload.humidity
        mock_iot_service.telemetry["soilPH"] = payload.ph
        mock_iot_service.telemetry["nitrogenLevel"] = payload.nitrogen
        mock_iot_service.telemetry["phosphorusLevel"] = payload.phosphorus
        mock_iot_service.telemetry["potassiumLevel"] = payload.potassium
        if payload.solar_radiation is not None:
            mock_iot_service.telemetry["solarRadiation"] = payload.solar_radiation
        if payload.soil_ec is not None:
            mock_iot_service.telemetry["soilEC"] = payload.soil_ec

        if payload.soil_moisture < 35.0:
            mock_iot_service.telemetry["soilMoistureStatus"] = "Deficit (પાણીની જરૂર)"
        elif payload.soil_moisture > 55.0:
            mock_iot_service.telemetry["soilMoistureStatus"] = "Surplus (વધુ પડતો ભેજ)"
        else:
            mock_iot_service.telemetry["soilMoistureStatus"] = "Optimal (પૂરતો ભેજ)"

        # 3. Persist reading to PostgreSQL / SQLite
        reading_id = str(uuid.uuid4())
        if db:
            reading = SensorReading(
                id=reading_id,
                sensor_id=sensor_id,
                field_id=field_id,
                soil_moisture=payload.soil_moisture,
                soil_temperature=payload.temperature,
                soil_ph=payload.ph,
                soil_ec=payload.soil_ec or 0.42,
                nitrogen=payload.nitrogen,
                phosphorus=payload.phosphorus,
                potassium=payload.potassium,
                air_temperature=payload.temperature,
                air_humidity=payload.humidity,
                timestamp=datetime.now(timezone.utc),
                recorded_at=datetime.now(timezone.utc)
            )
            db.add(reading)

            # Update sensor node last_sync
            res = await db.execute(select(SensorNode).where(SensorNode.id == sensor_id))
            node = res.scalars().first()
            if node:
                node.last_sync = "Just now"
                node.status = "Online"

            try:
                await db.commit()
            except Exception as e:
                await db.rollback()
                logger.error(f"Failed to persist sensor reading: {e}")

        # 4. Broadcast live sensor update via WebSocket to frontend
        await ws_manager.broadcast_to_farm(farm_id, "sensor_update", {
            "farm_id": farm_id,
            "field_id": field_id,
            "sensor_id": sensor_id,
            "telemetry": mock_iot_service.get_current_telemetry(),
            "timestamp": payload.timestamp
        })

        # 5. Check if water stress requires risk alert broadcast
        if payload.soil_moisture < 35.0:
            await ws_manager.broadcast_to_farm(farm_id, "risk_detected", {
                "field_id": field_id,
                "risk_type": "Water Deficit Stress",
                "severity": "High",
                "soil_moisture": payload.soil_moisture,
                "message": f"Critical soil moisture deficit ({payload.soil_moisture}%) detected in {field_id}. Immediate irrigation advised."
            })

        return {
            "status": "success",
            "reading_id": reading_id,
            "soil_moisture": payload.soil_moisture,
            "validated": True
        }

    async def execute_valve_cycle(
        self,
        farm_id: str,
        field_id: str,
        device_id: str = "VALVE-01",
        duration_minutes: int = 35,
        task_id: Optional[str] = None,
        db: Optional[AsyncSession] = None
    ) -> Dict[str, Any]:
        """
        Full 5-phase Valve State Machine:
        1. MQTT command: OPEN
        2. Valve state: RUNNING
        3. Duration complete timer
        4. MQTT command: CLOSE -> Valve state: CLOSED
        5. Task state: COMPLETED + Activity Log
        """
        field_key = "fieldA" if "a" in field_id.lower() else "fieldB" if "b" in field_id.lower() else "fieldC"

        # Step 1: Send MQTT command to open valve
        await self.provider.send_command(
            farm_id=farm_id,
            field_id=field_id,
            device_id=device_id,
            command="OPEN",
            params={"duration_minutes": duration_minutes}
        )

        # Step 2: Update state to RUNNING
        self.valve_states[field_key] = "Running"
        mock_iot_service.valve_active[field_key] = True
        if field_key == "fieldA":
            mock_iot_service.telemetry["dripValveA"] = "Running"
        elif field_key == "fieldB":
            mock_iot_service.telemetry["dripValveB"] = "Running"
        else:
            mock_iot_service.telemetry["dripValveC"] = "Running"

        await ws_manager.broadcast_to_farm(farm_id, "valve_status", {
            "field_id": field_id,
            "device_id": device_id,
            "status": "Running",
            "active_valves": self.valve_states
        })

        if task_id and db:
            res = await db.execute(select(FarmTask).where(FarmTask.id == task_id))
            task = res.scalars().first()
            if task:
                task.status = "In Progress"
                await db.commit()

        # Step 3: Launch asynchronous background cycle
        sim_task = asyncio.create_task(
            self._valve_duration_timer(farm_id, field_id, field_key, device_id, duration_minutes, task_id, db)
        )
        self.active_valve_tasks[field_key] = sim_task

        logger.info(f"Solenoid Valve {device_id} in {field_id} is now RUNNING for {duration_minutes} mins.")
        return {
            "status": "Running",
            "field_id": field_id,
            "device_id": device_id,
            "duration_minutes": duration_minutes,
            "valve_state": "Running"
        }

    async def _valve_duration_timer(
        self,
        farm_id: str,
        field_id: str,
        field_key: str,
        device_id: str,
        duration_minutes: int,
        task_id: Optional[str],
        db: Optional[AsyncSession]
    ):
        try:
            # Scaled simulation duration for demo responsiveness (e.g. 2-3 seconds)
            await asyncio.sleep(2)
            
            # Simulated absorption: moisture increases
            mock_iot_service.telemetry["soilMoisture"] = 38.5
            mock_iot_service.telemetry["soilMoistureStatus"] = "Moistening (ભેજ વધી રહ્યો છે)"
            await ws_manager.broadcast_to_farm(farm_id, "sensor_update", {
                "telemetry": mock_iot_service.get_current_telemetry(),
                "field_id": field_id
            })

            await asyncio.sleep(2)
            # Step 4: Valve duration completes -> Send MQTT CLOSE command
            await self.provider.send_command(
                farm_id=farm_id,
                field_id=field_id,
                device_id=device_id,
                command="CLOSE"
            )

            self.valve_states[field_key] = "Closed"
            mock_iot_service.valve_active[field_key] = False
            if field_key == "fieldA":
                mock_iot_service.telemetry["dripValveA"] = "Closed"
                mock_iot_service.telemetry["soilMoisture"] = 46.2
                mock_iot_service.telemetry["soilMoistureStatus"] = "Optimal (પૂરતો ભેજ)"
                mock_iot_service.telemetry["farmHealthScore"] = 89

            # Step 5: Mark Task as COMPLETED
            if task_id and db:
                res = await db.execute(select(FarmTask).where(FarmTask.id == task_id))
                task = res.scalars().first()
                if task:
                    task.status = "Completed"
                    await db.commit()

            # Step 6: Log activity record
            if db:
                audit = ActivityLog(
                    id=f"LOG-{uuid.uuid4().hex[:4].upper()}",
                    farm_id=farm_id,
                    time=datetime.now(timezone.utc).strftime("%I:%M %p"),
                    agent="Execution Agent",
                    event=f"Automated Drip Irrigation Completed for {field_id}",
                    severity="success"
                )
                db.add(audit)
                try:
                    await db.commit()
                except Exception:
                    pass

            # Step 7: Broadcast completed statuses via WebSocket
            await ws_manager.broadcast_to_farm(farm_id, "valve_status", {
                "field_id": field_id,
                "device_id": device_id,
                "status": "Closed",
                "active_valves": self.valve_states
            })
            await ws_manager.broadcast_to_farm(farm_id, "task_updated", {
                "task_id": task_id,
                "status": "Completed",
                "field_id": field_id
            })
            await ws_manager.broadcast_to_farm(farm_id, "sensor_update", {
                "telemetry": mock_iot_service.get_current_telemetry(),
                "field_id": field_id
            })
            logger.info(f"Valve {device_id} cycle finished. Soil moisture normalized to {mock_iot_service.telemetry['soilMoisture']}%.")
        except asyncio.CancelledError:
            self.valve_states[field_key] = "Closed"
            mock_iot_service.valve_active[field_key] = False
            logger.info(f"Valve cycle cancelled for {field_id}")

iot_service = IoTService()
