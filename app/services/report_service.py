from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, date
from app.models.erp_models import Order, OrderItem, Product, Client

class ReportService:
    def __init__(self, db: Session):
        self.db = db

    def get_dashboard_stats(self):
        """Obtiene métricas generales para las tarjetas del dashboard."""
        # Total ventas ($)
        total_sales = self.db.query(func.sum(Order.total_amount)).scalar() or 0.0
        
        # Pedidos de HOY (Conteo)
        today = date.today()
        orders_today = self.db.query(Order).filter(func.date(Order.date) == today).count()

        return {
            "total_sales": total_sales,
            "orders_today": orders_today, # Nuevo
            "total_clients": self.db.query(Client).count(),
            "total_products": self.db.query(Product).count(),
            "low_stock_alert": self.db.query(Product).filter(Product.stock < 10).count()
        }

    def get_recent_orders(self, limit: int = 5):
        """Obtiene las últimas órdenes creadas."""
        orders = self.db.query(Order).order_by(desc(Order.date)).limit(limit).all()
        # Formateamos para el frontend
        return [
            {
                "id": o.id,
                "client": o.client.name if o.client else "Cliente Desconocido",
                "date": o.date.strftime("%d/%m/%Y"),
                "total": o.total_amount,
                "status": "Entregado" # Simulado, podrías agregar un campo status al modelo
            }
            for o in orders
        ]

    def get_low_stock(self):
        """Obtiene la lista de productos con stock crítico (menor a 10)."""
        products = self.db.query(Product).filter(Product.stock < 10).all()
        return [
            {
                "id": p.id,
                "name": p.name,
                "stock": p.stock, 
                "price": p.price,
                "category": "General" # Simulado
            } for p in products
        ]

    def get_top_products(self, limit: int = 5):
        results = self.db.query(
            Product.name, 
            func.sum(OrderItem.quantity).label('sold')
        ).join(OrderItem).group_by(Product.id).order_by(desc('sold')).limit(limit).all()
        return [{"product": r.name, "sold": r.sold} for r in results]