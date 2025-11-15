from fastapi import APIRouter
<<<<<<< Updated upstream
=======
from .sync_routes import router as sync_router

>>>>>>> Stashed changes
router = APIRouter()

# Rutas generales
@router.get("/api/health")
def health_check():
    return {"status": "ok", "service": "ERP Backend"}

# Registrar módulo de sincronización
router.include_router(sync_router, prefix="/api/sync", tags=["Sync"])
