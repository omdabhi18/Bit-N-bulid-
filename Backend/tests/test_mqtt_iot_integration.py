import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.integrations.mqtt_client import MQTTTopicBuilder, MockIoTProvider, get_iot_provider
from app.services.iot_service import iot_service

def test_mqtt_topic_builder():
    topic = MQTTTopicBuilder.telemetry_topic("farm-01", "field-A", "SOIL-001")
    assert topic == "farm/farm-01/field/field-A/sensor/SOIL-001/telemetry"
    
    status_topic = MQTTTopicBuilder.device_status_topic("farm-01", "field-A", "VALVE-01")
    assert status_topic == "farm/farm-01/field/field-A/device/VALVE-01/status"
    
    cmd_topic = MQTTTopicBuilder.device_command_topic("farm-01", "field-A", "VALVE-01")
    assert cmd_topic == "farm/farm-01/field/field-A/device/VALVE-01/command"
    
    parsed = MQTTTopicBuilder.parse_topic(topic)
    assert parsed["farm_id"] == "farm-01"
    assert parsed["field_id"] == "field-A"
    assert parsed["type"] == "sensor"
    assert parsed["id"] == "SOIL-001"
    assert parsed["action"] == "telemetry"

@pytest.mark.asyncio
async def test_telemetry_valid_payload_ingestion():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {
            "device_id": "SOIL-001",
            "soil_moisture": 31.4,
            "temperature": 32.5,
            "humidity": 61.0,
            "ph": 6.4,
            "nitrogen": 72.0,
            "phosphorus": 51.0,
            "potassium": 68.0
        }
        response = await client.post("/api/sensors/telemetry", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["soil_moisture"] == 31.4

@pytest.mark.asyncio
async def test_telemetry_rejects_impossible_values():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Moisture > 100% is impossible
        bad_payload = {
            "device_id": "SOIL-001",
            "soil_moisture": 150.0,
            "temperature": 32.5,
            "humidity": 61.0,
            "ph": 6.4,
            "nitrogen": 72.0,
            "phosphorus": 51.0,
            "potassium": 68.0
        }
        response = await client.post("/api/sensors/telemetry", json=bad_payload)
        assert response.status_code == 422

@pytest.mark.asyncio
async def test_valve_execution_lifecycle():
    res = await iot_service.execute_valve_cycle(
        farm_id="farm-greenvalley-01",
        field_id="fieldA",
        device_id="VALVE-01",
        duration_minutes=35
    )
    assert res["status"] == "Running"
    assert res["valve_state"] == "Running"
