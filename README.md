# ERP Backend – Sincronización Offline → Online

Este proyecto implementa un sistema de sincronización para clientes móviles/web que pueden trabajar sin conexión y enviar datos al servidor cuando vuelven online.

Incluye:
- FastAPI
- SQLAlchemy
- PostgreSQL
- Servicios de sincronización (push/pull)
- Manejo de dispositivos
- Cola de sincronización
- Testing con pytest & httpx

---

## 🚀 Requisitos Previos

Antes de iniciar, asegúrate de tener instalado:

- Python 3.10+
- PostgreSQL
- Git

---

## 📦 Instalación de Dependencias

Ejecuta los siguientes comandos en este orden:

### 1. Actualizar pip
```bash
py -m pip install --upgrade pip
py -m venv venv
venv\Scripts\activate
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv python-dateutil
```
### 2. Pruebas Test
```bash
pip install pytest pytest-asyncio httpx
pip install pytest pytest-asyncio httpx
```
