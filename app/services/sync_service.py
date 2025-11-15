from datetime import datetime
from sqlalchemy.orm import Session
from app.models.sync import SyncQueue
from app.models.device import Device


def ensure_device(db: Session, device_id: str):
    device = db.query(Device).filter(Device.device_id == device_id).first()
    if not device:
        device = Device(device_id=device_id)
        db.add(device)
        db.commit()
        db.refresh(device)
    return device


def handle_push(data: dict, db: Session):
    device_id = data.get("device_id")
    entity = data.get("entity")
    payload = data.get("payload")

    # Registrar el device si no existe
    ensure_device(db, device_id)

    # Verificar si existe un registro previo con el mismo entity+id
    existing = (
        db.query(SyncQueue)
        .filter(
            SyncQueue.entity == entity,
            SyncQueue.payload["id"].as_integer() == payload["id"]
        )
        .order_by(SyncQueue.created_at.desc())
        .first()
    )

    # Si existe, comparamos updated_at (last write wins)
    if existing:
        if "updated_at" in payload and "updated_at" in existing.payload:
            new_time = datetime.fromisoformat(payload["updated_at"])
            old_time = datetime.fromisoformat(existing.payload["updated_at"])

            if new_time <= old_time:
                return {
                    "status": "ignored",
                    "reason": "older_or_equal_update"
                }

    # Insert nuevo registro a la cola
    item = SyncQueue(
        entity=entity,
        payload=payload,
        device_id=device_id,
    )
    db.add(item)
    db.commit()
    db.refresh(item)

    return {"status": "queued", "id": item.id}


def handle_pull(data: dict, db: Session):
    device_id = data.get("device_id")

    # Registrar si no existe
    device = ensure_device(db, device_id)

    updates = (
        db.query(SyncQueue)
        .filter(SyncQueue.synced_at == None)
        .all()
    )

    # Marcar como sincronizados
    now = datetime.utcnow()
    for u in updates:
        u.synced_at = now

    # Actualizar last_sync en devices
    device.last_sync = now

    db.commit()

    return {"updates": [u.payload for u in updates]}


def get_sync_status(device_id: str, db: Session):
    device = db.query(Device).filter(Device.device_id == device_id).first()

    if not device:
        return {"status": "device_not_registered"}

    return {
        "device_id": device.device_id,
        "last_sync": device.last_sync,
        "registered_at": device.registered_at,
    }
