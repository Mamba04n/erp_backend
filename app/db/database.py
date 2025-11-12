import os
from typing import Generator

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


load_dotenv()

# Read individual Postgres variables (use sensible defaults if not provided)
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "85503301")
POSTGRES_DB = os.getenv("POSTGRES_DB", "erp_db")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

# Allow an explicit DATABASE_URL to override the composed one
DATABASE_URL = os.getenv(
	"DATABASE_URL",
	f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}",
)

# SQLAlchemy engine and session factory
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative base for models
Base = declarative_base()


def get_db() -> Generator:
	"""Yield a SQLAlchemy session and ensure it is closed after use."""
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


def init_db() -> None:
	"""Create database tables for all registered models (if they don't exist)."""
	# Import models here so they are registered on the metadata before create_all()
	# from app import models  # uncomment/adjust when you add model modules
	Base.metadata.create_all(bind=engine)
