from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.sync import SyncQueue
from datetime import datetime
from typing import List, Dict, Any


def handle_push(data: List[Dict[str, Any]], db: Session):
    """
    Inserta los datos recibidos desde el cliente offline.
    """
    inserted_count = 0
    for item in data:
        record = SyncQueue(
            entity=item.get("entity"),
            payload=item.get("payload"),
            device_id=item.get("device_id"),
        )
        db.add(record)
        inserted_count += 1
    db.commit()
    return inserted_count


def handle_pull(device_id: str, db: Session):
    """
    Devuelve actualizaciones simuladas.
    Más adelante, aquí puedes integrar la lógica real de actualización desde el ERP.
    """
    # Ejemplo simulado: registros del propio dispositivo aún no sincronizados
    updates = (
        db.query(SyncQueue)
        .filter(SyncQueue.device_id == device_id, SyncQueue.synced_at.is_(None))
        .all()
    )

    # Convertir a diccionario serializable
    result = [
        {
            "id": u.id,
            "entity": u.entity,
            "payload": u.payload,
            "created_at": u.created_at,
        }
        for u in updates
    ]

    # Marcar como sincronizados
    for u in updates:
        u.synced_at = datetime.utcnow()
    db.commit()

    return result


def get_sync_status(device_id: str, db: Session):
    """
    Devuelve el timestamp del último registro sincronizado para el dispositivo.
    """
    last_sync = (
        db.query(func.max(SyncQueue.synced_at))
        .filter(SyncQueue.device_id == device_id)
        .scalar()
    )
    return last_sync
