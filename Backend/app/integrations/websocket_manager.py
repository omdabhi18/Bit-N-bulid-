from fastapi import WebSocket
from typing import Dict, List
import json
from app.utils.logger import logger

class WebSocketManager:
    def __init__(self):
        # Maps farm_id -> list of active WebSockets
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, farm_id: str, websocket: WebSocket):
        await websocket.accept()
        if farm_id not in self.active_connections:
            self.active_connections[farm_id] = []
        self.active_connections[farm_id].append(websocket)
        logger.info(f"WebSocket client connected to farm '{farm_id}'. Active: {len(self.active_connections[farm_id])}")

    def disconnect(self, farm_id: str, websocket: WebSocket):
        if farm_id in self.active_connections:
            if websocket in self.active_connections[farm_id]:
                self.active_connections[farm_id].remove(websocket)
            if not self.active_connections[farm_id]:
                del self.active_connections[farm_id]
        logger.info(f"WebSocket client disconnected from farm '{farm_id}'")

    async def broadcast_to_farm(self, farm_id: str, event_type: str, data: dict):
        if farm_id not in self.active_connections:
            return
        payload = json.dumps({"type": event_type, "data": data})
        stale_connections = []
        for connection in self.active_connections[farm_id]:
            try:
                await connection.send_text(payload)
            except Exception as e:
                logger.warning(f"Error broadcasting WebSocket message: {e}")
                stale_connections.append(connection)
        for dead_conn in stale_connections:
            self.disconnect(farm_id, dead_conn)

ws_manager = WebSocketManager()
