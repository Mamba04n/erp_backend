# app/models/__init__.py

# Importa los modelos para que se registren en Base.metadata
from app.models.sync_log import SyncLog 
 # noqa: F401
from app.models.clients import Client  # noqa: F401
from app.models.orders import Order, OrderItem  # noqa: F401
from app.models.products import Product  # noqa: F401