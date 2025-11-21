# app/api/ws_routes.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.core.events import manager

router = APIRouter()


@router.websocket("/ws/updates")
async def websocket_updates(websocket: WebSocket):
    # Cliente se conecta
    await manager.connect(websocket)
    try:
        # Mantener la conexión viva
        while True:
            # Puedes leer pings del cliente si quieres
            _ = await websocket.receive_text()
    except WebSocketDisconnect:
        # Cliente se desconectó
        await manager.disconnect(websocket)
