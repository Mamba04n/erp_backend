from typing import Callable, Dict, List, Any
from asyncio import iscoroutinefunction
import json

from app.db import get_db
from app.models.sync_log import SyncLog


class EventBus:
    """
    Sistema de eventos simple que permite registrar listeners
    y emitir eventos asincrónicos.
    """

    def __init__(self):
        self.listeners: Dict[str, List[Callable]] = {}

    def subscribe(self, event_name: str, callback: Callable):
        """
        Registrar un listener (función que se ejecuta cuando se emite un evento).
        """
        if event_name not in self.listeners:
            self.listeners[event_name] = []
        self.listeners[event_name].append(callback)

    async def emit(self, event_name: str, payload: Any):
        """
        Emitir un evento a todos los listeners.
        """

        # ---------------------------------------------------
        # 1. Registrar log automático del evento
        # ---------------------------------------------------
        try:
            db = next(get_db())
            log_entry = SyncLog(
                action=f"event.{event_name}",
                entity_type="event",
                entity_id="N/A",
                status="success",
                details_json=json.dumps(payload or {}),
            )
            db.add(log_entry)
            db.commit()
        except Exception as e:
            print("⚠ Error registrando log de evento:", e)

        # ---------------------------------------------------
        # 2. Ejecutar listeners registrados
        # ---------------------------------------------------
        if event_name not in self.listeners:
            return

        for callback in self.listeners[event_name]:
            if iscoroutinefunction(callback):
                await callback(payload)
            else:
                callback(payload)


# Instancia global del EventBus
event_bus = EventBus()


# ---------------------------------------------------
# Función de log_sync accesible desde todo el proyecto
# ---------------------------------------------------
def log_sync(
    db,
    action: str,
    entity_type: str,
    entity_id: str,
    status: str = "success",
    details: dict | None = None,
):
    entry = SyncLog(
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
        details_json=json.dumps(details or {}),
    )
    db.add(entry)
        details_json=json.dumps(details or {}, ensure_ascii=False),
    )
    db.add(log)
    db.commit()
