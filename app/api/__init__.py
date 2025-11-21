# app/api/__init__.py
from fastapi import APIRouter

from app.api.ws_routes import router as ws_router
from app.api.clients import router as clients_router
from app.api.orders import router as orders_router
from app.api.products import router as products_router

router = APIRouter()

# Rutas HTTP normales
@router.get("/api/health")
def health_check():
    return {"status": "ok", "service": "ERP Backend"}

# Rutas WebSocket
router.include_router(ws_router)
router.include_router(clients_router)
router.include_router(orders_router)
router.include_router(products_router)