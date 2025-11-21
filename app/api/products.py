# app/api/products.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.db import get_db
from app.models.products import Product
from app.core.events import event_bus, log_sync   # <-- Usamos event_bus

router = APIRouter(prefix="/products", tags=["products"])


# -----------------------------
# Schemas
# -----------------------------

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


# -----------------------------
# Crear producto
# -----------------------------

@router.post("/", response_model=ProductOut)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    product = Product(name=payload.name, stock=payload.stock)
    db.add(product)
    db.commit()
    db.refresh(product)

    # Puedes registrar log si lo deseas, pero lo dejé como estaba:
    # log_sync(...)

    return product


# -----------------------------
# Listar productos
# -----------------------------

@router.get("/", response_model=list[ProductOut])
def list_products(db: Session = Depends(get_db)):
    return db.query(Product).all()


# -----------------------------
# Actualizar stock con logs y eventos
# -----------------------------

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

    # ---------------------------------------------------------
    # Registrar log del cambio de stock (tu lógica original)
    # ---------------------------------------------------------
    log_sync(
        db=db,
        action="product.stock_changed",
        entity_type="product",
        entity_id=product.id,
        status="success",
        details={"old_stock": old_stock, "new_stock": product.stock},
    )

    # ---------------------------------------------------------
    # Emitir evento estándar via EventBus
    # ---------------------------------------------------------
    await event_bus.emit("stock_changed", {
        "event": "stock_changed",
        "data": {
            "product_id": product.id,
            "old_stock": old_stock,
            "new_stock": product.stock
        }
    })

    # ---------------------------------------------------------
    # Evento adicional si el producto queda sin stock
    # ---------------------------------------------------------
    if product.stock == 0:

        log_sync(
            db=db,
            action="product.out_of_stock",
            entity_type="product",
            entity_id=product.id,
            status="success",
            details={},
        )

        await event_bus.emit("product_out_of_stock", {
            "event": "product_out_of_stock",
            "data": {
                "product_id": product.id
            }
        })

    return product
