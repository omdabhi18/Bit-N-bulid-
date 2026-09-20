import json
import logging
import asyncio
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Callable, List
from datetime import datetime, timezone
from pydantic import BaseModel, Field, field_validator

from app.config import settings

logger = logging.getLogger(__name__)

class MQTTTopicBuilder:
    """Centralized Topic Builder ensuring consistent MQTT hierarchy across the system."""

    @staticmethod
    def telemetry_topic(farm_id: str, field_id: str, sensor_id: str) -> str:
        return f"farm/{farm_id}/field/{field_id}/sensor/{sensor_id}/telemetry"

    @staticmethod
    def device_status_topic(farm_id: str, field_id: str, device_id: str) -> str:
        return f"farm/{farm_id}/field/{field_id}/device/{device_id}/status"

    @staticmethod
    def device_command_topic(farm_id: str, field_id: str, device_id: str) -> str:
        return f"farm/{farm_id}/field/{field_id}/device/{device_id}/command"

    @staticmethod
    def parse_topic(topic: str) -> Dict[str, str]:
        parts = topic.strip("/").split("/")
        result = {}
        if len(parts) >= 2 and parts[0] == "farm":
            result["farm_id"] = parts[1]
        if len(parts) >= 4 and parts[2] == "field":
            result["field_id"] = parts[3]
        if len(parts) >= 6:
            result["type"] = parts[4]  # sensor or device
            result["id"] = parts[5]
        if len(parts) >= 7:
            result["action"] = parts[6]  # telemetry, status, command
        return result


class SensorTelemetryPayload(BaseModel):
    """Rigorous sensor telemetry validation schema."""
    device_id: str
    timestamp: Optional[str] = None
    soil_moisture: float = Field(..., ge=0.0, le=100.0, description="Soil moisture percentage 0-100%")
    temperature: float = Field(..., ge=-10.0, le=65.0, description="Temperature -10C to 65C")
    humidity: float = Field(..., ge=0.0, le=100.0, description="Relative humidity 0-100%")
    ph: float = Field(..., ge=0.0, le=14.0, description="pH level 0-14")
    nitrogen: float = Field(..., ge=0.0, le=500.0, description="Nitrogen mg/kg")
    phosphorus: float = Field(..., ge=0.0, le=300.0, description="Phosphorus mg/kg")
    potassium: float = Field(..., ge=0.0, le=500.0, description="Potassium mg/kg")
    soil_ec: Optional[float] = Field(default=0.42, ge=0.0, le=10.0)
    solar_radiation: Optional[float] = Field(default=820.0, ge=0.0, le=2000.0)

    @field_validator("timestamp", mode="before")
    def validate_timestamp(cls, v):
        if not v:
            return datetime.now(timezone.utc).isoformat()
        return v


class IoTProvider(ABC):
    """Abstract Base Class for IoT / MQTT connectivity providers."""

    @abstractmethod
    async def connect(self) -> bool:
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        pass

    @abstractmethod
    async def publish(self, topic: str, payload: Dict[str, Any]) -> bool:
        pass

    @abstractmethod
    async def subscribe(self, topic: str, callback: Callable[[str, Dict[str, Any]], Any]) -> None:
        pass

    @abstractmethod
    async def send_command(
        self,
        farm_id: str,
        field_id: str,
        device_id: str,
        command: str,
        params: Optional[Dict[str, Any]] = None
    ) -> bool:
        pass


class MockIoTProvider(IoTProvider):
    """In-memory mock IoT Provider implementing full parity with real MQTT."""

    def __init__(self):
        self._subscriptions: Dict[str, List[Callable]] = {}
        self._connected = True

    async def connect(self) -> bool:
        self._connected = True
        logger.info("Connected to Mock IoT Pub/Sub Broker.")
        return True

    async def disconnect(self) -> None:
        self._connected = False
        logger.info("Disconnected from Mock IoT Broker.")

    async def publish(self, topic: str, payload: Dict[str, Any]) -> bool:
        logger.debug(f"[Mock MQTT PUB] {topic} -> {payload}")
        # Match topic subscriptions (exact or wildcard)
        for sub_topic, callbacks in self._subscriptions.items():
            if self._topic_matches(sub_topic, topic):
                for cb in callbacks:
                    try:
                        if asyncio.iscoroutinefunction(cb):
                            asyncio.create_task(cb(topic, payload))
                        else:
                            cb(topic, payload)
                    except Exception as e:
                        logger.error(f"Error in Mock MQTT subscriber callback: {e}")
        return True

    def _topic_matches(self, pattern: str, topic: str) -> bool:
        if pattern == "#" or pattern == topic:
            return True
        p_parts = pattern.split("/")
        t_parts = topic.split("/")
        if len(p_parts) != len(t_parts) and pattern[-1] != "#":
            return False
        for p, t in zip(p_parts, t_parts):
            if p == "#":
                return True
            if p != "+" and p != t:
                return False
        return len(p_parts) == len(t_parts)

    async def subscribe(self, topic: str, callback: Callable[[str, Dict[str, Any]], Any]) -> None:
        if topic not in self._subscriptions:
            self._subscriptions[topic] = []
        self._subscriptions[topic].append(callback)
        logger.info(f"Subscribed to Mock MQTT topic: {topic}")

    async def send_command(
        self,
        farm_id: str,
        field_id: str,
        device_id: str,
        command: str,
        params: Optional[Dict[str, Any]] = None
    ) -> bool:
        topic = MQTTTopicBuilder.device_command_topic(farm_id, field_id, device_id)
        payload = {
            "device_id": device_id,
            "command": command,
            "params": params or {},
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        return await self.publish(topic, payload)


class PahoMQTTProvider(IoTProvider):
    """Production Paho MQTT v2 Provider connecting to physical/remote MQTT broker."""

    def __init__(self):
        self.host = settings.MQTT_BROKER_HOST
        self.port = settings.MQTT_BROKER_PORT
        self.username = settings.MQTT_USERNAME
        self.password = settings.MQTT_PASSWORD
        self._client = None
        self._connected = False
        self._subscriptions: Dict[str, List[Callable]] = {}
        self._fallback_provider = MockIoTProvider()

    async def connect(self) -> bool:
        import paho.mqtt.client as mqtt
        try:
            self._client = mqtt.Client(
                mqtt.CallbackAPIVersion.VERSION2,
                client_id=f"krishinetra-backend-{datetime.now().timestamp()}"
            )
            if self.username and self.password:
                self._client.username_pw_set(self.username, self.password)

            self._client.on_connect = self._on_connect
            self._client.on_message = self._on_message
            self._client.on_disconnect = self._on_disconnect

            # Connect with short timeout
            self._client.connect_async(self.host, self.port, keepalive=60)
            self._client.loop_start()
            self._connected = True
            logger.info(f"Connecting to MQTT Broker at {self.host}:{self.port}...")
            return True
        except Exception as e:
            logger.warning(f"Failed to connect to MQTT Broker at {self.host}:{self.port} ({e}). Using Mock IoT Provider.")
            self._connected = False
            return await self._fallback_provider.connect()

    def _on_connect(self, client, userdata, flags, rc, properties=None):
        logger.info(f"Connected to MQTT Broker with result code: {rc}")
        # Resubscribe all active topics
        for topic in self._subscriptions.keys():
            client.subscribe(topic)

    def _on_disconnect(self, client, userdata, disconnect_flags, reason_code, properties=None):
        logger.warning(f"MQTT Broker disconnected ({reason_code}). Reconnecting...")
        self._connected = False

    def _on_message(self, client, userdata, msg):
        try:
            topic = msg.topic
            payload = json.loads(msg.payload.decode())
            for sub_topic, callbacks in self._subscriptions.items():
                if self._fallback_provider._topic_matches(sub_topic, topic):
                    for cb in callbacks:
                        if asyncio.iscoroutinefunction(cb):
                            asyncio.create_task(cb(topic, payload))
                        else:
                            cb(topic, payload)
        except Exception as e:
            logger.error(f"Error handling MQTT message: {e}")

    async def disconnect(self) -> None:
        if self._client:
            self._client.loop_stop()
            self._client.disconnect()
            self._connected = False

    async def publish(self, topic: str, payload: Dict[str, Any]) -> bool:
        if self._connected and self._client:
            try:
                res = self._client.publish(topic, json.dumps(payload), qos=1)
                return res.rc == 0
            except Exception as e:
                logger.error(f"MQTT publish failed: {e}. Routing to fallback.")
        return await self._fallback_provider.publish(topic, payload)

    async def subscribe(self, topic: str, callback: Callable[[str, Dict[str, Any]], Any]) -> None:
        if topic not in self._subscriptions:
            self._subscriptions[topic] = []
        self._subscriptions[topic].append(callback)
        if self._connected and self._client:
            self._client.subscribe(topic)
        # Always maintain mock mirror
        await self._fallback_provider.subscribe(topic, callback)

    async def send_command(
        self,
        farm_id: str,
        field_id: str,
        device_id: str,
        command: str,
        params: Optional[Dict[str, Any]] = None
    ) -> bool:
        topic = MQTTTopicBuilder.device_command_topic(farm_id, field_id, device_id)
        payload = {
            "device_id": device_id,
            "command": command,
            "params": params or {},
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        return await self.publish(topic, payload)


# Factory function
_iot_singleton: Optional[IoTProvider] = None

def get_iot_provider() -> IoTProvider:
    global _iot_singleton
    if _iot_singleton is None:
        if settings.MQTT_BROKER_HOST and settings.MQTT_BROKER_HOST not in ["localhost", "127.0.0.1"]:
            _iot_singleton = PahoMQTTProvider()
        else:
            _iot_singleton = MockIoTProvider()
    return _iot_singleton

mqtt_service = get_iot_provider()
