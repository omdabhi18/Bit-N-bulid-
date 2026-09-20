import asyncio
import random
from typing import Dict, Any
from app.integrations.websocket_manager import ws_manager
from app.utils.logger import logger

class MockIoTDeviceService:
    def __init__(self):
        self.telemetry = {
            "farmHealthScore": 82,
            "soilMoisture": 31.4,
            "soilMoistureStatus": "Deficit (પાણીની જરૂર)",
            "soilTemperature": 27.8,
            "soilPH": 6.8,
            "soilEC": 0.42,
            "nitrogenLevel": 82.0,
            "phosphorusLevel": 14.0,
            "potassiumLevel": 185.0,
            "airTemperature": 33.2,
            "airHumidity": 58.0,
            "rainfallProb24h": 12,
            "windSpeed": 14.0,
            "solarRadiation": 820.0,
            "dripValveA": "Closed",
            "dripValveB": "Standby",
            "dripValveC": "Closed"
        }
        self.valve_active = {
            "fieldA": False,
            "fieldB": False,
            "fieldC": False
        }
        self.running_simulation_tasks: Dict[str, asyncio.Task] = {}

    def get_current_telemetry(self) -> Dict[str, Any]:
        return self.telemetry.copy()

    def get_valve_status(self) -> Dict[str, bool]:
        return self.valve_active.copy()

    async def trigger_solenoid_valve(self, farm_id: str, field_id: str, minutes: int = 35) -> Dict[str, Any]:
        field_key = "fieldA" if "a" in field_id.lower() else "fieldB" if "b" in field_id.lower() else "fieldC"
        self.valve_active[field_key] = True
        
        if field_key == "fieldA":
            self.telemetry["dripValveA"] = "Running"
        elif field_key == "fieldB":
            self.telemetry["dripValveB"] = "Running"
        else:
            self.telemetry["dripValveC"] = "Running"

        # Broadcast live valve status
        await ws_manager.broadcast_to_farm(farm_id, "valve_status", {
            "fieldId": field_id,
            "status": "Running",
            "activeValves": self.valve_active
        })

        # Launch async task to simulate water absorption
        task = asyncio.create_task(self._simulate_irrigation_cycle(farm_id, field_id, field_key, minutes))
        self.running_simulation_tasks[field_key] = task

        logger.info(f"Mock Solenoid Valve opened for {field_id} ({minutes} mins scheduled)")
        return {
            "status": "Running",
            "fieldId": field_id,
            "minutes": minutes,
            "valveState": self.valve_active
        }

    async def _simulate_irrigation_cycle(self, farm_id: str, field_id: str, field_key: str, minutes: int):
        try:
            # Step 1: Moisture starts rising
            await asyncio.sleep(2)
            if field_key == "fieldA":
                self.telemetry["soilMoisture"] = 38.5
                self.telemetry["soilMoistureStatus"] = "Moistening (ભેજ વધી રહ્યો છે)"
            
            await ws_manager.broadcast_to_farm(farm_id, "sensor_update", {
                "telemetry": self.telemetry,
                "fieldId": field_id
            })

            # Step 2: Target optimal moisture achieved
            await asyncio.sleep(3)
            if field_key == "fieldA":
                self.telemetry["soilMoisture"] = 46.2
                self.telemetry["soilMoistureStatus"] = "Optimal (પૂરતો ભેજ)"
                self.telemetry["farmHealthScore"] = 89
                self.telemetry["dripValveA"] = "Closed"
            
            self.valve_active[field_key] = False

            await ws_manager.broadcast_to_farm(farm_id, "sensor_update", {
                "telemetry": self.telemetry,
                "fieldId": field_id
            })
            await ws_manager.broadcast_to_farm(farm_id, "valve_status", {
                "fieldId": field_id,
                "status": "Completed",
                "activeValves": self.valve_active
            })
            logger.info(f"Irrigation completed for {field_id}. Soil moisture normalized to {self.telemetry['soilMoisture']}%")
        except asyncio.CancelledError:
            self.valve_active[field_key] = False
            logger.info(f"Irrigation simulation cancelled for {field_id}")

    def stop_valve(self, farm_id: str, field_id: str):
        field_key = "fieldA" if "a" in field_id.lower() else "fieldB" if "b" in field_id.lower() else "fieldC"
        self.valve_active[field_key] = False
        if field_key == "fieldA":
            self.telemetry["dripValveA"] = "Closed"
        if field_key in self.running_simulation_tasks:
            self.running_simulation_tasks[field_key].cancel()

mock_iot_service = MockIoTDeviceService()
