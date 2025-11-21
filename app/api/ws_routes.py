from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core.events import manager

# Esta instancia de 'router' es necesaria para que main.py pueda incluirla
router = APIRouter()

@router.websocket("/ws/updates")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Mantiene la conexión viva esperando mensajes (aunque no hagamos nada con ellos)
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)