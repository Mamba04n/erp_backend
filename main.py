import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.db.database import init_db

# Importar todas las rutas
from app.api import ws_routes, report_routes, product_routes, order_routes, auth_routes, client_routes

# Inicializar DB
init_db()

app = FastAPI(title="FRIDAYS ERP - Full System")

# Configuración Frontend
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# REGISTRAR RUTAS API
app.include_router(auth_routes.router)
app.include_router(ws_routes.router)
app.include_router(report_routes.router)
app.include_router(product_routes.router)
app.include_router(order_routes.router)
app.include_router(client_routes.router) # <-- IMPORTANTE: Esta línea registra los clientes

# RUTAS DE NAVEGACIÓN (PÁGINAS)
@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse('login.html', {"request": request})

@app.get("/", response_class=FileResponse)
def read_root():
    dashboard_path = os.path.join("templates", "dashboard.html")
    if os.path.exists(dashboard_path):
        return FileResponse(dashboard_path)
    return FileResponse("dashboard.html")

@app.get('/clientes')
def clientes_page(request: Request):
    return templates.TemplateResponse('clientes.html', {"request": request})

@app.get('/clientes.html')
def clientes_page_html(request: Request):
    return templates.TemplateResponse('clientes.html', {"request": request})

@app.get('/pedidos')
def pedidos_page(request: Request):
    return templates.TemplateResponse('pedidos.html', {"request": request})

@app.get('/pedidos.html')
def pedidos_page_html(request: Request):
    return templates.TemplateResponse('pedidos.html', {"request": request})

@app.get('/facturacion')
def facturacion_page(request: Request):
    return templates.TemplateResponse('facturizacion.html', {"request": request})

@app.get('/facturacion.html')
def facturacion_page_html(request: Request):
    return templates.TemplateResponse('facturizacion.html', {"request": request})

@app.get('/productos')
def productos_page(request: Request):
    return templates.TemplateResponse('productos.html', {"request": request})

@app.get('/productos.html')
def productos_page_html(request: Request):
    return templates.TemplateResponse('productos.html', {"request": request})