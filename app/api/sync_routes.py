from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.db.database import get_db
from app.models.sync import SyncQueue
from app.services import sync_service

router = APIRouter(prefix="/sync", tags=["Sync"])


@router.post("/push")
def push_sync(data: List[Dict[str, Any]], db: Session = Depends(get_db)):
    """
    Recibe datos creados o modificados offline.
    Los guarda temporalmente en la tabla sync_queue.
    """
    if not data:
        raise HTTPException(status_code=400, detail="No se recibieron datos para sincronizar")

    inserted = sync_service.handle_push(data, db)
    return {"status": "success", "inserted": inserted}


@router.post("/pull")
def pull_sync(device_id: str, db: Session = Depends(get_db)):
    """
    Devuelve actualizaciones para el dispositivo.
    Por ahora simula una respuesta (mock).
    """
    updates = sync_service.handle_pull(device_id, db)
    return {"status": "success", "updates": updates}


@router.get("/status/{device_id}")
def sync_status(device_id: str, db: Session = Depends(get_db)):
    """
    Devuelve el estado del último sync para un dispositivo.
    """
    status = sync_service.get_sync_status(device_id, db)
    if not status:
        raise HTTPException(status_code=404, detail="No hay registros de sincronización para este dispositivo")
    return {"device_id": device_id, "last_sync": status}
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.services.sync_service import (
    handle_push,
    handle_pull,
    get_sync_status
)

router = APIRouter()

@router.post("/push")
def sync_push(data: dict, db: Session = Depends(get_db)):
    return handle_push(data, db)

@router.post("/pull")
def sync_pull(data: dict, db: Session = Depends(get_db)):
    return handle_pull(data, db)

@router.get("/status/{device_id}")
def sync_status(device_id: str, db: Session = Depends(get_db)):
    return get_sync_status(device_id, db)
