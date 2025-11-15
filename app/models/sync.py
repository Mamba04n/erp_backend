<<<<<<< Updated upstream
from sqlalchemy import Column, Integer, String, JSON, DateTime, func
from app.db.database import Base
=======
from sqlalchemy import Column, Integer, String, JSON, DateTime
from datetime import datetime
from app.db import Base
>>>>>>> Stashed changes

class SyncQueue(Base):
    __tablename__ = "sync_queue"

    id = Column(Integer, primary_key=True, index=True)
<<<<<<< Updated upstream
    entity = Column(String, nullable=False)        # Nombre de la entidad (ej: "cliente", "pedido")
    payload = Column(JSON, nullable=False)         # Datos serializados del cambio offline
    device_id = Column(String, nullable=False)     # Identificador del dispositivo que envía el dato
    synced_at = Column(DateTime, nullable=True)    # Cuándo se sincronizó con éxito
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
=======
    entity = Column(String, nullable=False)
    payload = Column(JSON, nullable=False)
    device_id = Column(String, nullable=False)

    synced_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
>>>>>>> Stashed changes
