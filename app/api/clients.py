# app/api/clients.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from app.db import get_db
from app.models.clients import Client

router = APIRouter(prefix="/clients", tags=["clients"])


class ClientCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str | None = None


class ClientOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str | None = None

    class Config:
        orm_mode = True


@router.post("/", response_model=ClientOut)
def create_client(payload: ClientCreate, db: Session = Depends(get_db)):
    existing = db.query(Client).filter_by(email=payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    client = Client(
        name=payload.name,
        email=payload.email,
        phone=payload.phone,
    )
    db.add(client)
    db.commit()
    db.refresh(client)
    return client


@router.get("/", response_model=list[ClientOut])
def list_clients(db: Session = Depends(get_db)):
    return db.query(Client).all()
