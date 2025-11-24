from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.models.erp_models import Client, User
from app.schemas import ClientCreate, ClientResponse
from app.core.security import get_current_sales_person

router = APIRouter(prefix="/clients", tags=["Clientes"])

@router.get("/", response_model=List[ClientResponse])
def list_clients(db: Session = Depends(get_db)):
    return db.query(Client).all()

@router.post("/", response_model=ClientResponse)
def create_client(
    client: ClientCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_sales_person)
):
    existing = db.query(Client).filter(Client.email == client.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Ya existe un cliente con ese email")
    
    new_client = Client(
        name=client.name,
        email=client.email,
        contact=client.contact,
        address=client.address,
        zone=client.zone
    )
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client

@router.get("/{client_id}", response_model=ClientResponse)
def get_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return client