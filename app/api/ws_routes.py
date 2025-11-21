from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List
import json

from app.core.events import event_bus

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_personal(self, message: dict, websocket: WebSocket):
        await websocket.send_text(json.dumps(message))

    async def broadcast(self, message: dict):
        msg = json.dumps(message)
        for connection in self.active_connections:
            await connection.send_text(msg)


manager = ConnectionManager()


# Listener que envía eventos a los clientes conectados
async def websocket_event_listener(payload):
    await manager.broadcast(payload)


# Registramos los eventos que queremos enviar por WebSocket
event_bus.subscribe("order_created", websocket_event_listener)
event_bus.subscribe("stock_changed", websocket_event_listener)
event_bus.subscribe("product_out_of_stock", websocket_event_listener)


@router.websocket("/ws/updates")
async def websocket_updates(websocket: WebSocket):
    """
    WebSocket para notificaciones en tiempo real
    """
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()

            # opcional: eco del mensaje
            await manager.send_personal(
                {"event": "echo", "data": data},
                websocket
            )

    except WebSocketDisconnect:
        manager.disconnect(websocket)
