from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth import verify_api_key
from app.database.database import get_db
from app.schemas.ligne_commande import (
    LigneCommandeCreate,
    LigneCommandeUpdate,
)
from app.services.ligne_commande_service import (
    add_ligne,
    get_lignes_commande,
    update_ligne,
    delete_ligne,
)

router = APIRouter(
    prefix="/commandes",
    tags=["Lignes de commande"],
    dependencies=[Depends(verify_api_key)],
)

@router.post("/{commande_id}/lignes", status_code=201)
def create_ligne(
    commande_id: int,
    ligne_data: LigneCommandeCreate,
    db: Session = Depends(get_db),
):
    try:
        return add_ligne(
            db,
            commande_id,
            ligne_data,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
    
@router.get("/{commande_id}/lignes")
def read_lignes_commande(
    commande_id: int,
    db: Session = Depends(get_db),
):
    try:
        return get_lignes_commande(db, commande_id)
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

@router.patch("/lignes/{ligne_id}", status_code=201)
def update_ligne_route(
    ligne_id: int,
    ligne_data: LigneCommandeUpdate,
    db: Session = Depends(get_db),
):
    try:
        return update_ligne(
            db,
            ligne_id,
            ligne_data,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.delete("/lignes/{ligne_id}", status_code=201)
def delete_ligne_route(
    ligne_id: int,
    db: Session = Depends(get_db),
):
    try:
        delete_ligne(db, ligne_id)

        return {
            "message": "Ligne de commande supprimée avec succès."
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )