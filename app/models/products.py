from sqlalchemy import Column, Integer, String
from app.db import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    stock = Column(Integer, default=0)
