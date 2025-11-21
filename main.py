import os
from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.db.database import init_db, get_db
from app.models.erp_models import SyncLog
from app.core.events import manager

# --- IMPORTAR RUTAS (Incluyendo Auth) ---
from app.api import ws_routes, report_routes, product_routes, order_routes, auth_routes

# Inicializar DB (Crea tablas si no existen)
init_db()

app = FastAPI(title="FRIDAYS ERP - Full System")

# --- CONFIGURACIÓN DE FRONTEND ---
# 1. Montar carpeta 'static' para CSS/JS/Imágenes
app.mount("/static", StaticFiles(directory="static"), name="static")

# 2. Configurar carpeta 'templates' para HTMLs dinámicos
templates = Jinja2Templates(directory="templates")

# --- MIDDLEWARE (CORS) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- REGISTRAR RUTAS API ---
app.include_router(auth_routes.router)    # Seguridad (Login/Token)
app.include_router(ws_routes.router)      # WebSockets (Alertas)
app.include_router(report_routes.router)  # Reportes y Datos
app.include_router(product_routes.router) # Gestión de Productos
app.include_router(order_routes.router)   # Gestión de Órdenes

# --- RUTAS DE NAVEGACIÓN (PÁGINAS HTML) ---

# 1. Pantalla de Login
@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse('login.html', {"request": request})

# 2. Dashboard Principal (Raíz)
@app.get("/", response_class=FileResponse)
def read_root():
    # Servimos el dashboard.html. La protección real (redirigir si no hay token)
    # se hace dentro del HTML con JavaScript.
    dashboard_path = os.path.join("templates", "dashboard.html")
    if os.path.exists(dashboard_path):
        return FileResponse(dashboard_path)
    # Fallback si el archivo está en la raíz
    return FileResponse("dashboard.html")

# 3. Clientes
@app.get('/clientes')
def clientes_page(request: Request):
    return templates.TemplateResponse('clientes.html', {"request": request})

@app.get('/clientes.html')
def clientes_page_html(request: Request):
    return templates.TemplateResponse('clientes.html', {"request": request})

# 4. Pedidos
@app.get('/pedidos')
def pedidos_page(request: Request):
    return templates.TemplateResponse('pedidos.html', {"request": request})

@app.get('/pedidos.html')
def pedidos_page_html(request: Request):
    return templates.TemplateResponse('pedidos.html', {"request": request})

# 5. Facturación
@app.get('/facturacion')
def facturacion_page(request: Request):
    return templates.TemplateResponse('facturizacion.html', {"request": request})

@app.get('/facturacion.html')
def facturacion_page_html(request: Request):
    return templates.TemplateResponse('facturizacion.html', {"request": request})