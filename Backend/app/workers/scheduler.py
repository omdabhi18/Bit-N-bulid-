import asyncio
from app.utils.logger import logger
from app.integrations.mock_iot import mock_iot_service
from app.integrations.websocket_manager import ws_manager

async def periodic_telemetry_jitter(farm_id: str = "farm-greenvalley-01"):
    """
    Background worker simulating realistic sensor micro-fluctuations
    and broadcasting updates via WebSocket.
    """
    logger.info("Starting background periodic telemetry scheduler...")
    while True:
        try:
            await asyncio.sleep(45) # every 45 seconds
            telemetry = mock_iot_service.get_current_telemetry()
            await ws_manager.broadcast_to_farm(farm_id, "sensor_update", {
                "telemetry": telemetry,
                "timestamp": "Just now"
            })
        except asyncio.CancelledError:
            logger.info("Periodic telemetry scheduler cancelled.")
            break
        except Exception as e:
            logger.warning(f"Error in periodic telemetry loop: {e}")
            await asyncio.sleep(10)
