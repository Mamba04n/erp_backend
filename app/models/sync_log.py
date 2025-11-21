# app/models/sync_log.py
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Text
from app.db import Base  # usamos el Base que ya define tu proyecto


class SyncLog(Base):
    __tablename__ = "sync_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # Qué pasó
    action = Column(String(100), index=True)        # ej: 'order.created', 'product.stock_changed'
    entity_type = Column(String(50), index=True)    # ej: 'order', 'product'
    entity_id = Column(String(64), index=True)      # ej: '123', 'SKU-99'

    # Resultado
    status = Column(String(20), default="success")  # 'success' | 'error'
    details_json = Column(Text, nullable=True)      # JSON con detalles

    # Cuándo
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
