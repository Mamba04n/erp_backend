import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from sqlalchemy.orm import Session
from app.db.database import init_db, get_db
from app.models.erp_models import SyncLog
from app.core.events import manager

# --- IMPORTAR NUEVAS RUTAS ---
from app.api import ws_routes, report_routes, product_routes, order_routes

# Inicializar DB
init_db()

app = FastAPI(title="ERP System - Full Version")

# Montar archivos estáticos y plantillas
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- REGISTRAR TODAS LAS RUTAS ---
app.include_router(ws_routes.router)
app.include_router(report_routes.router)
app.include_router(product_routes.router)
app.include_router(order_routes.router)


# --- RUTAS DE INTERFAZ (TEMPLATES) ---
@app.get("/", response_class=FileResponse)
def read_root():
    dashboard_path = os.path.join("templates", "dashboard.html")
    if os.path.exists(dashboard_path):
        return FileResponse(dashboard_path)
    return FileResponse("templates/dashboard.html")


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

@app.get('/facturizacion')
def facturizacion_page(request: Request):
    return templates.TemplateResponse('facturizacion.html', {"request": request})

@app.get('/facturacion.html')
def facturacion_page_html(request: Request):
    return templates.TemplateResponse('facturizacion.html', {"request": request})

@app.get('/facturizacion.html')
def facturizacion_page_html(request: Request):
    return templates.TemplateResponse('facturizacion.html', {"request": request})