from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# --- Esquemas de Producto ---
class ProductBase(BaseModel):
    name: str
    price: float
    stock: int

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    class Config:
        from_attributes = True # Antes orm_mode

# --- Esquemas de Orden ---
class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int

class OrderCreate(BaseModel):
    client_id: int
    items: List[OrderItemCreate]

class OrderResponse(BaseModel):
    id: int
    total_amount: float
    date: datetime
    class Config:
        from_attributes = True