from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.erp_models import Product, SyncLog
from app.schemas.schemas import ProductCreate, ProductResponse
from app.core.events import manager

router = APIRouter(prefix="/products", tags=["Productos"])

@router.post("/", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    new_product = Product(name=product.name, price=product.price, stock=product.stock)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@router.put("/{id}/stock")
async def update_stock(id: int, quantity: int, db: Session = Depends(get_db)):
    """Actualiza el stock y envía alerta en tiempo real."""
    product = db.query(Product).filter(Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # Actualizar stock
    product.stock = quantity
    
    # Registrar Log
    log = SyncLog(entity="Product", action="update_stock", details=f"Product {id} stock -> {quantity}")
    db.add(log)
    db.commit()

    # --- NOTIFICACIÓN REAL ---
    # Si el stock es bajo, enviamos alerta específica, si no, actualización general
    event_type = "LOW_STOCK_WARNING" if quantity < 10 else "STOCK_UPDATE"
    await manager.broadcast_event(event_type, {
        "product_id": id,
        "product_name": product.name,
        "new_stock": quantity
    })

    return {"message": "Stock actualizado", "new_stock": quantity}

@router.get("/", response_model=list[ProductResponse])
def list_products(db: Session = Depends(get_db)):
    return db.query(Product).all()