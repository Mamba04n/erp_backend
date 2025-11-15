from sqlalchemy import Column, String, DateTime
from datetime import datetime
from app.db.database import Base

class Device(Base):
    __tablename__ = "devices"

    device_id = Column(String, primary_key=True, index=True)
    last_sync = Column(DateTime, nullable=True)
    registered_at = Column(DateTime, default=datetime.utcnow)
