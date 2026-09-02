from decimal import Decimal
from math import ceil
from fastapi import Depends

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.auth import verify_api_key
from app.database.database import get_db
from app.models.commande import StatutCommande
from app.schemas.commande import (
    CommandeCreate, 
    CommandeUpdate, 
    CommandeResponse
)
from app.schemas.common import PaginatedResponse
from app.services.commande_service import (
    create_commande,
    get_commande,
    get_commandes,
    update_commande,
)


router = APIRouter(
    prefix="/commandes", 
    tags=["Commandes"],
    dependencies=[Depends(verify_api_key)],
    )


@router.get(
    "",
    response_model=PaginatedResponse[CommandeResponse]
)
def list_commandes(
    client_id: int | None = None,
    statut: StatutCommande | None = None,
    montant_min: Decimal | None = None,
    montant_max: Decimal | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    commandes, total = get_commandes(
        db=db,
        client_id=client_id,
        statut=statut,
        montant_min=montant_min,
        montant_max=montant_max,
        page=page,
        page_size=page_size,
    )

    pages = ceil(total / page_size) if total > 0 else 0

    return {
        "items": commandes,
        "total": total,
        "page": page,
        "page_size": page_size,
        "pages": pages,
    }

@router.post("", status_code=201)
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


@router.patch("/{commande_id}/statut", status_code=200)
def update_statut(
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