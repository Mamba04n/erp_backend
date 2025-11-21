🚀 FRIDAYS ERP

Sistema backend para la gestión de una distribuidora (Inventario, Ventas, Alertas en Tiempo Real).

⚡ Guía de Inicio Rápido

Sigue estos pasos exactos para levantar el proyecto en tu máquina local.

1. Prerrequisitos

Python 3.9+ instalado.

PostgreSQL instalado y corriendo.

2. Instalación

# 1. Clonar el repositorio
git clone [https://github.com/tu-usuario/fridays-erp.git](https://github.com/tu-usuario/fridays-erp.git)
cd fridays-erp

# 2. Crear entorno virtual (Recomendado)
python -m venv venv
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt


3. Configuración

Crea un archivo .env en la raíz con tus credenciales de PostgreSQL:

POSTGRES_USER=postgres
POSTGRES_PASSWORD=tu_password
POSTGRES_DB=erp_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432


Importante: Asegúrate de crear la base de datos vacía llamada erp_db en tu gestor de SQL antes de continuar.

4. Carga de Datos (Seed)

Para llenar la base de datos con productos y clientes de prueba:

python seed.py


(Escribe 's' si te pide confirmar).

5. Ejecutar

uvicorn main:app --reload


🖥️ Acceso

Una vez corriendo, abre tu navegador en:

Dashboard (Frontend): http://127.0.0.1:8000

Documentación API (Swagger): http://127.0.0.1:8000/docs
