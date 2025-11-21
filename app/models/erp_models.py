from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Boolean, Date
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime
import enum

# --- Enums del Negocio ---
class SyncStatus(str, enum.Enum):
    SUCCESS = "success"
    FAILED = "failed"
    PENDING = "pending"

class OrderStatus(str, enum.Enum): # RF-11
    PENDIENTE = "pendiente"
    PREPARADO = "preparado"
    EN_RUTA = "en_ruta"
    ENTREGADO = "entregado"

class UserRole(str, enum.Enum): # RF-19
    ADMIN = "administrador"
    VENDEDOR = "vendedor"
    REPARTIDOR = "repartidor"

# --- Tabla de Usuarios (RF-19 & RNF-04) ---
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String) # RNF-04: Encriptado
    role = Column(String, default=UserRole.VENDEDOR) # admin, vendedor, repartidor
    is_active = Column(Boolean, default=True)

# --- Tablas del Negocio ---
class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    contact = Column(String, nullable=True) # RF-01
    address = Column(String, nullable=True) # RF-01
    zone = Column(String, nullable=True)    # RF-02: Zona de entrega (Rivas, Tola, etc.)
    email = Column(String)
    orders = relationship("Order", back_populates="client")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(String, nullable=True) # RF-04
    stock = Column(Integer)
    price = Column(Float)
    expiry_date = Column(Date, nullable=True) # RF-04: Fecha caducidad
    order_items = relationship("OrderItem", back_populates="product")

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.utcnow)
    total_amount = Column(Float, default=0.0)
    status = Column(String, default=OrderStatus.PENDIENTE) # RF-11
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

class SyncLog(Base):
    __tablename__ = "sync_logs"
    id = Column(Integer, primary_key=True, index=True)
    entity = Column(String, index=True)
    action = Column(String)
    details = Column(String, nullable=True)
    status = Column(String, default=SyncStatus.SUCCESS)
    timestamp = Column(DateTime, default=datetime.utcnow)