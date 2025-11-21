# app/api/orders.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.db import get_db
from app.models.orders import Order, OrderItem
from app.models.clients import Client
from app.models.products import Product
from app.core.events import emit_event, log_sync

router = APIRouter(prefix="/orders", tags=["orders"])


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int


class OrderCreate(BaseModel):
    client_id: int
    items: list[OrderItemCreate]


class OrderItemOut(BaseModel):
    id: int
    product_id: int
    quantity: int

    class Config:
        orm_mode = True


class OrderOut(BaseModel):
    id: int
    client_id: int
    items: list[OrderItemOut]

    class Config:
        orm_mode = True


@router.post("/", response_model=OrderOut)
async def create_order(payload: OrderCreate, db: Session = Depends(get_db)):
    # verificar cliente
    client = db.query(Client).filter_by(id=payload.client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    if not payload.items:
        raise HTTPException(status_code=400, detail="Order must have at least one item")

    # verificar productos
    product_ids = [item.product_id for item in payload.items]
    products = db.query(Product).filter(Product.id.in_(product_ids)).all()
    products_map = {p.id: p for p in products}

    for item in payload.items:
        if item.product_id not in products_map:
            raise HTTPException(
                status_code=404,
                detail=f"Product {item.product_id} not found",
            )

    # crear orden
    order = Order(client_id=client.id)
    db.add(order)
    db.commit()
    db.refresh(order)

    # crear items
    for item in payload.items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
        )
        db.add(order_item)

    db.commit()
    db.refresh(order)

    # log en sync_logs
    log_sync(
        db=db,
        action="order.created",
        entity_type="order",
        entity_id=order.id,
        status="success",
        details={
            "client_id": client.id,
            "items": [
                {"product_id": i.product_id, "quantity": i.quantity}
                for i in order.items
            ],
        },
    )

    # evento WS
    await emit_event(
        "order.created",
        {
            "order_id": order.id,
            "client_id": client.id,
            "items_count": len(order.items),
        },
    )

    return order


@router.get("/", response_model=list[OrderOut])
def list_orders(db: Session = Depends(get_db)):
    orders = db.query(Order).all()
    return orders
