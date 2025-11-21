from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.erp_models import Order, OrderItem, Product, SyncLog, User
from app.schemas import OrderCreate, OrderResponse
from app.core.events import manager
# Importamos la nueva dependencia de permisos
from app.core.security import get_current_sales_person 

router = APIRouter(prefix="/orders", tags=["Órdenes"])

@router.post("/", response_model=OrderResponse)
async def create_order(
    order_data: OrderCreate, 
    db: Session = Depends(get_db),
    # CAMBIO AQUÍ: Usamos get_current_sales_person en lugar de get_current_user
    current_user: User = Depends(get_current_sales_person) 
):
    print(f"Orden autorizada por: {current_user.username} ({current_user.role})")
    
    # 1. Crear la orden cabecera
    new_order = Order(client_id=order_data.client_id, total_amount=0)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    total = 0.0
    items_details = []

    # 2. Procesar items y descontar stock
    for item in order_data.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            continue 
        
        if product.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Stock insuficiente para {product.name}")

        # Descontar stock
        product.stock -= item.quantity
        subtotal = product.price * item.quantity
        total += subtotal

        # Crear item
        db_item = OrderItem(
            order_id=new_order.id,
            product_id=product.id,
            quantity=item.quantity,
            subtotal=subtotal
        )
        db.add(db_item)
        items_details.append(f"{product.name} (x{item.quantity})")

    # 3. Actualizar total
    new_order.total_amount = total
    
    # 4. Log de Auditoría (Incluye quién lo hizo)
    log = SyncLog(
        entity="Order", 
        action="create", 
        details=f"Order #{new_order.id} by {current_user.username}. Total: ${total}"
    )
    db.add(log)
    db.commit()

    # 5. Notificación
    await manager.broadcast_event("NEW_ORDER", {
        "order_id": new_order.id,
        "total": total,
        "items": items_details,
        "created_by": current_user.username
    })

    return new_order