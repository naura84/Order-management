from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.services.commande_service import (
    create_commande,
    get_commande,
    get_commandes,
    update_commande
)
from app.schemas.commande import CommandeCreate, CommandeUpdate

router = APIRouter(
    prefix="/commandes", 
    tags=["Commandes"]
    )

@router.post("/")
def create(
    commande_data: CommandeCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_commande(db, commande_data)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get("/")
def read_commandes(
    db: Session = Depends(get_db),
):
    return get_commandes(db)


@router.get("/{commande_id}")
def read_commande(
    commande_id: int,
    db: Session = Depends(get_db),
):
    try:
        return get_commande(db, commande_id)
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )


@router.patch("/{commande_id}")
def update(
    commande_id: int,
    commande_data: CommandeUpdate,
    db: Session = Depends(get_db),
):
    try:
        return update_commande(
            db,
            commande_id,
            commande_data,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )