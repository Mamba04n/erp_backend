import sys
from sqlalchemy import text

print("🚀 Iniciando script de semilla (Versión Distribuidora)...")

try:
    from app.db.database import SessionLocal, init_db, engine
    from app.models.erp_models import Client, Product, Order, OrderItem, SyncLog, Base
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    sys.exit(1)

import random
from datetime import datetime, timedelta

def clean_database(db):
    """Borra todos los datos existentes para empezar de cero."""
    print("🧹 Limpiando base de datos antigua...")
    try:
        # Orden importante por las llaves foráneas
        db.execute(text("TRUNCATE TABLE sync_logs RESTART IDENTITY CASCADE;"))
        db.execute(text("TRUNCATE TABLE order_items RESTART IDENTITY CASCADE;"))
        db.execute(text("TRUNCATE TABLE orders RESTART IDENTITY CASCADE;"))
        db.execute(text("TRUNCATE TABLE products RESTART IDENTITY CASCADE;"))
        db.execute(text("TRUNCATE TABLE clients RESTART IDENTITY CASCADE;"))
        db.commit()
        print("✨ Base de datos limpia.")
    except Exception as e:
        print(f"⚠️ No se pudo limpiar automáticamente (quizás es la primera vez): {e}")
        db.rollback()

def seed_data():
    print("🔌 Conectando a PostgreSQL...")
    db = SessionLocal()
    
    try:
        # Verificar si hay datos viejos
        existing_product = db.query(Product).first()
        if existing_product:
            print(f"⚠️ Se encontraron datos (Ej: {existing_product.name}).")
            respuesta = input("¿Quieres BORRAR todo y cargar los datos de la Distribuidora? (s/n): ")
            if respuesta.lower() == 's':
                clean_database(db)
            else:
                print("Cancelado. No se hicieron cambios.")
                return

        print("🌱 Insertando catálogo de Distribuidora de Granos Básicos...")

        # 1. Crear Clientes (Pulperías y Negocios)
        print("   > Registrando Clientes (Pulperías)...")
        clients_data = [
            ("Pulpería La Bendición", "pedidos@labendicion.com"),
            ("Mercadito El Centro", "compras@mercadito.com"),
            ("Abarrotes Doña María", "maria.rodriguez@hotmail.com"),
            ("Comedor Los Hermanos", "abastecimiento@comedorhnos.com"),
            ("Mini Super El Económico", "contacto@eleconomico.ni")
        ]
        
        clients = []
        for name, email in clients_data:
            c = Client(name=name, email=email)
            db.add(c)
            clients.append(c)
        db.commit()

        # 2. Crear Productos (Granos y Hogar)
        print("   > Ingresando Inventario (Quintales y Cajas)...")
        products = []
        # Formato: (Nombre, Precio, Stock Actual)
        items = [
            ("Arroz Faisán 96/4 (Quintal)", 1200.0, 150),
            ("Frijoles Rojos (Quintal)", 1800.0, 80),
            ("Azúcar Refinada (Saco 50lb)", 850.0, 200),
            ("Aceite Vegetal (Bidón 20L)", 1100.0, 50),
            ("Jabón de Lavar (Caja 24u)", 380.0, 100),
            ("Cloro Líquido (Caja 12 Galones)", 450.0, 40),
            ("Café Molido (Paquete 12u)", 650.0, 60),
            ("Papel Higiénico (Fardo 48 rollos)", 520.0, 120),
            ("Harina de Maíz (Saco 50lb)", 700.0, 45),
            ("Salsa de Tomate (Caja 24u)", 320.0, 90)
        ]
        
        for name, price, stock in items:
            p = Product(name=name, price=price, stock=stock)
            db.add(p)
            products.append(p)
        db.commit()

        # 3. Crear Órdenes Históricas
        print("   > Generando historial de pedidos...")
        # Recargamos objetos para asegurar IDs
        for c in clients: db.refresh(c)
        for p in products: db.refresh(p)

        for _ in range(25): 
            client = random.choice(clients)
            # Fechas aleatorias últimos 3 meses
            date = datetime.utcnow() - timedelta(days=random.randint(0, 90))
            
            order = Order(client_id=client.id, date=date, total_amount=0)
            db.add(order)
            db.commit() 
            db.refresh(order)

            total = 0
            num_items = random.randint(1, 4) # Pedidos variados
            
            for _ in range(num_items):
                prod = random.choice(products)
                qty = random.randint(1, 10) # Cantidad de sacos/cajas
                
                if prod.stock < qty: qty = 1 

                subtotal = prod.price * qty
                
                item = OrderItem(
                    order_id=order.id,
                    product_id=prod.id,
                    quantity=qty,
                    subtotal=subtotal
                )
                db.add(item)
                total += subtotal
            
            order.total_amount = total
            db.add(order)
        
        db.commit()
        print("✅ ¡DATOS DE DISTRIBUIDORA CARGADOS EXITOSAMENTE!")

    except Exception as e:
        print(f"❌ ERROR: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
    seed_data()