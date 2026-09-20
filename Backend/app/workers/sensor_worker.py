import asyncio
import logging
from typing import Dict, Any

from app.integrations.mqtt_client import get_iot_provider, MQTTTopicBuilder
from app.services.iot_service import iot_service
from app.database import AsyncSessionLocal

logger = logging.getLogger(__name__)

class SensorWorker:
    """Background consumer worker for MQTT telemetry and device status messages."""

    def __init__(self):
        self.provider = get_iot_provider()
        self._running = False

    async def start(self):
        self._running = True
        await self.provider.connect()
        # Subscribe to wildcard telemetry topics
        telemetry_wildcard = "farm/+/field/+/sensor/+/telemetry"
        await self.provider.subscribe(telemetry_wildcard, self.handle_telemetry_message)
        logger.info(f"SensorWorker started. Listening on {telemetry_wildcard}")

    async def stop(self):
        self._running = False
        await self.provider.disconnect()
        logger.info("SensorWorker stopped.")

    async def handle_telemetry_message(self, topic: str, payload: Dict[str, Any]):
        parsed = MQTTTopicBuilder.parse_topic(topic)
        farm_id = parsed.get("farm_id", "farm-01")
        field_id = parsed.get("field_id", "field-cotton-01")
        sensor_id = parsed.get("id", payload.get("device_id", "SN-Cotton-01"))

        logger.info(f"Worker received MQTT telemetry from {sensor_id} on {topic}")
        async with AsyncSessionLocal() as db:
            try:
                await iot_service.process_sensor_payload(
                    farm_id=farm_id,
                    field_id=field_id,
                    sensor_id=sensor_id,
                    payload_data=payload,
                    db=db
                )
            except Exception as e:
                logger.error(f"Error processing sensor telemetry payload in worker: {e}")

sensor_worker = SensorWorker()
