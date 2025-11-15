import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Generator

# Load environment variables
load_dotenv()

# Read Postgres variables
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "12345")
POSTGRES_DB = os.getenv("POSTGRES_DB", "erp_db")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

# Compose database URL
DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

# DEBUG prints (opcionales)
print("USER:", repr(POSTGRES_USER))
print("PASS:", repr(POSTGRES_PASSWORD))
print("HOST:", repr(POSTGRES_HOST))
print("DB:", repr(POSTGRES_DB))
print("PORT:", repr(POSTGRES_PORT))
print("URL:", repr(DATABASE_URL))

# SQLAlchemy engine/session setup
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative base
Base = declarative_base()

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db() -> None:
<<<<<<< Updated upstream
	"""Create database tables for all registered models (if they don't exist)."""
	# Import models here so they are registered on the metadata before create_all()
	# from app import models  # uncomment/adjust when you add model modules
	from app.models import sync 
	Base.metadata.create_all(bind=engine)
=======
    # Import models so SQLAlchemy registers them
    from app.models import sync
    from app.models import device
    Base.metadata.create_all(bind=engine)
>>>>>>> Stashed changes
