import sys
import random
from datetime import datetime, timedelta
from sqlalchemy import text

print("🚀 Iniciando script de semilla (Distribuidora FRIDAYS)...")

try:
    from app.db.database import SessionLocal, init_db
    from app.models.erp_models import Client, Product, Order, OrderItem, User, OrderStatus, UserRole
    try:
        from app.core.security import get_password_hash
    except ImportError:
        print("⚠️ Advertencia: No se pudo importar passlib. Usando hash simulado.")
        def get_password_hash(p): return f"hashed_{p}"
        
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    sys.exit(1)

def clean_database(db):
    print("🧹 Limpiando base de datos...")
    try:
        tables = ["sync_logs", "order_items", "orders", "products", "clients", "users"]
        for t in tables:
            db.execute(text(f"TRUNCATE TABLE {t} RESTART IDENTITY CASCADE;"))
        db.commit()
        print("✨ Base de datos limpia.")
    except Exception as e:
        print(f"⚠️ Error al limpiar: {e}")
        db.rollback()

def seed_data():
    print("🔌 Conectando a PostgreSQL...")
    db = SessionLocal()
    
    try:
        if db.query(User).first():
            res = input("⚠️ Ya existen datos. ¿Borrar todo y reiniciar con credenciales correctas? (s/n): ")
            if res.lower() == 's':
                clean_database(db)
            else:
                return

        print("🌱 Insertando datos...")

        # 1. USUARIOS (Con las contraseñas que pediste)
        print("   > Creando Usuarios...")
        users = [
            # Usuario, Email, Contraseña, Rol
            ("admin", "admin@fridays.com", "admin123", UserRole.ADMIN),
            ("vendedor", "ventas@fridays.com", "ventas123", UserRole.VENDEDOR),     # CORREGIDO
            ("repartidor", "ruta@fridays.com", "ruta123", UserRole.REPARTIDOR)      # CORREGIDO
        ]
        for user, email, pwd, role in users:
            u = User(
                username=user, 
                email=email, 
                hashed_password=get_password_hash(pwd), 
                role=role
            )
            db.add(u)
        db.commit()

        # 2. CLIENTES
        print("   > Creando Clientes...")
        clients_data = [
            ("Pulpería La Bendición", "Rivas", "Juan Pérez"),
            ("Mercadito El Centro", "Tola", "María López"),
            ("Abarrotes Doña Rosa", "Comunidades", "Rosa Martínez"),
            ("Comedor Los Hermanos", "Rivas", "Carlos Ruiz"),
            ("Mini Super El Económico", "Tola", "Ana Díaz")
        ]
        db_clients = []
        for name, zone, contact in clients_data:
            c = Client(name=name, zone=zone, contact=contact, email="cliente@test.com")
            db.add(c)
            db_clients.append(c)
        db.commit()

        # 3. PRODUCTOS
        print("   > Creando Productos...")
        products_data = [
            ("Arroz Faisán 96/4 (Quintal)", "Granos", 1200, 150),
            ("Frijol Rojo (Quintal)", "Granos", 1800, 80),
            ("Azúcar Refinada (Saco 50lb)", "Endulzantes", 850, 200),
            ("Aceite Vegetal (Bidón 20L)", "Aceites", 1100, 45),
            ("Jabón de Lavar (Caja 24u)", "Limpieza", 380, 100),
            ("Café Molido (Paquete 12u)", "Bebidas", 650, 60)
        ]
        expiry = datetime.now().date() + timedelta(days=180)
        
        db_products = []
        for name, cat, price, stock in products_data:
            p = Product(name=name, category=cat, price=price, stock=stock, expiry_date=expiry)
            db.add(p)
            db_products.append(p)
        db.commit()

        # 4. ÓRDENES
        print("   > Generando historial...")
        for c in db_clients: db.refresh(c)
        for p in db_products: db.refresh(p)
        
        statuses = [OrderStatus.ENTREGADO, OrderStatus.EN_RUTA, OrderStatus.PENDIENTE]

        for _ in range(15):
            client = random.choice(db_clients)
            date = datetime.utcnow() - timedelta(days=random.randint(0, 30))
            order = Order(client_id=client.id, date=date, total_amount=0, status=random.choice(statuses))
            db.add(order)
            db.commit()
            db.refresh(order)

            prod = random.choice(db_products)
            qty = random.randint(1, 5)
            item = OrderItem(order_id=order.id, product_id=prod.id, quantity=qty, subtotal=prod.price * qty)
            db.add(item)
            order.total_amount = item.subtotal
            db.add(order)
        
        db.commit()
        print("✅ ¡Datos cargados!")
        print("------------------------------------------------")
        print("🔑 CREDENCIALES:")
        print("   Admin:      admin      / admin123")
        print("   Vendedor:   vendedor   / ventas123")
        print("   Repartidor: repartidor / ruta123")
        print("------------------------------------------------")

    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
    seed_data()