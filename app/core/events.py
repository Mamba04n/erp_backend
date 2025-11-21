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
        action=action,
        entity_type=entity_type,
        entity_id=str(entity_id),
        status=status,
        details_json=json.dumps(details or {}),
    )
    db.add(entry)
    db.commit()
