from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, date

# ==============================
# 1. Esquemas de SEGURIDAD (Usuarios y Token)
# ==============================
class UserBase(BaseModel):
    username: str
    email: str
    role: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

# ==============================
# 2. Esquemas de PRODUCTOS
# ==============================
class ProductBase(BaseModel):
    name: str
    price: float
    stock: int
    category: Optional[str] = None
    expiry_date: Optional[date] = None

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    class Config:
        from_attributes = True

# ==============================
# 3. Esquemas de ÓRDENES
# ==============================
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
    status: str
    class Config:
        from_attributes = True