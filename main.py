from fastapi import FastAPI
from app.api import router as api_router

# Initialize DB
from app.db import init_db  # noqa: E402


app = FastAPI(title="ERP Backend", version="1.0")

app.include_router(api_router)

from app.api import ws_routes
app.include_router(ws_routes.router)



@app.on_event("startup")
def on_startup():
    # Initialize database (create tables). If you have models, ensure they're imported
    init_db()


@app.get("/")
def root():
    return {"message": "ERP Backend funcionando correctamente 🚀"}

