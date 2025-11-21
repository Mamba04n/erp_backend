# app/api/products.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.db import get_db
from app.models.products import Product
from app.core.events import emit_event, log_sync

router = APIRouter(prefix="/products", tags=["products"])


class ProductCreate(BaseModel):
    name: str
    stock: int = 0


class ProductOut(BaseModel):
    id: int
    name: str
    stock: int

    class Config:
        orm_mode = True


class StockUpdate(BaseModel):
    stock: int


@router.post("/", response_model=ProductOut)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    product = Product(name=payload.name, stock=payload.stock)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.get("/", response_model=list[ProductOut])
def list_products(db: Session = Depends(get_db)):
    return db.query(Product).all()


@router.put("/{product_id}/stock", response_model=ProductOut)
async def update_stock(
    product_id: int,
    payload: StockUpdate,
    db: Session = Depends(get_db),
):
    product = db.query(Product).filter_by(id=product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    old_stock = product.stock
    product.stock = payload.stock
    db.commit()
    db.refresh(product)

    # log en sync_logs
    log_sync(
        db=db,
        action="product.stock_changed",
        entity_type="product",
        entity_id=product.id,
        status="success",
        details={"old_stock": old_stock, "new_stock": product.stock},
    )

    # evento en WebSocket
    await emit_event(
        "product.stock_changed",
        {"product_id": product.id, "old_stock": old_stock, "new_stock": product.stock},
    )

    # si queda en 0, evento adicional
    if product.stock == 0:
        log_sync(
            db=db,
            action="product.out_of_stock",
            entity_type="product",
            entity_id=product.id,
            status="success",
            details={},
        )
        await emit_event(
            "product.out_of_stock",
            {"product_id": product.id},
        )

    return product
