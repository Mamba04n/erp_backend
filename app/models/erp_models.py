from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base
import enum

# --- Enums ---
class SyncStatus(str, enum.Enum):
    SUCCESS = "success"
    FAILED = "failed"
    PENDING = "pending"

# --- Log de Notificaciones ---
class SyncLog(Base):
    __tablename__ = "sync_logs"

    id = Column(Integer, primary_key=True, index=True)
    entity = Column(String, index=True)
    action = Column(String)
    details = Column(String, nullable=True)
    status = Column(String, default=SyncStatus.SUCCESS)
    timestamp = Column(DateTime, default=datetime.utcnow)

# --- Tablas del Negocio ---
class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    orders = relationship("Order", back_populates="client")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    stock = Column(Integer)
    price = Column(Float)
    order_items = relationship("OrderItem", back_populates="product")

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.utcnow)
    total_amount = Column(Float, default=0.0)
    client_id = Column(Integer, ForeignKey("clients.id"))
    
    client = relationship("Client", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    subtotal = Column(Float)

    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")