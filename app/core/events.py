# app/core/events.py
from typing import Any, Dict, List
import asyncio
import json
from datetime import datetime

from fastapi import WebSocket
from sqlalchemy.orm import Session

from app.models.sync_log import SyncLog


class ConnectionManager:
    """Administra las conexiones WebSocket y difunde eventos a todos."""
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self._lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        async with self._lock:
            self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        async with self._lock:
            if websocket in self.active_connections:
                self.active_connections.remove(websocket)

    async def broadcast(self, message: Dict[str, Any]):
        """Envía un mensaje JSON a todos los clientes conectados."""
        data = json.dumps(message, default=str)
        async with self._lock:
            to_remove = []
            for ws in self.active_connections:
                try:
                    await ws.send_text(data)
                except Exception:
                    to_remove.append(ws)
            for ws in to_remove:
                self.active_connections.remove(ws)


manager = ConnectionManager()

# Cola opcional por si luego quieres SSE u otros consumers
_event_queue: "asyncio.Queue[Dict[str, Any]]" = asyncio.Queue()


async def emit_event(event_type: str, payload: Dict[str, Any]):
    """
    Se llama desde tu lógica (crear orden, cambiar stock, etc.).
    Difunde el evento a todos los WebSockets conectados.
    """
    event = {
        "type": event_type,
        "payload": payload,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
    await manager.broadcast(event)
    await _event_queue.put(event)


def log_sync(
    db: Session,
    action: str,
    entity_type: str,
    entity_id: str | int,
    status: str = "success",
    details: Dict[str, Any] | None = None,
):
    """Registra en la tabla sync_logs qué se sincronizó y cómo salió."""
    log = SyncLog(
        action=action,
        entity_type=entity_type,
        entity_id=str(entity_id),
        status=status,
        details_json=json.dumps(details or {}, ensure_ascii=False),
    )
    db.add(log)
    db.commit()
