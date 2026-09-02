from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth import verify_api_key
from app.database.database import get_db
from app.schemas.client import ClientCreate, ClientUpdate
from app.services.client_service import (
    create_client,
    get_client,
    get_clients,
    get_client_by_email,
    update_client,
    delete_client,
    DuplicateEmailError,
)
from app.services.stat_service import get_stats_client

router = APIRouter(
    prefix="/clients",
    tags=["Clients"],
    dependencies=[Depends(verify_api_key)],
)

@router.post("", status_code=201)
def create(
    client_data: ClientCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_client(db, client_data)

    except DuplicateEmailError as e:
        raise HTTPException(
            status_code=409,
            detail=str(e),
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get("")
def read_clients(
    db: Session = Depends(get_db),
):
    return get_clients(db)


@router.get("/email/{email}")
def read_client_by_email(
    email: str,
    db: Session = Depends(get_db),
):
    client = get_client_by_email(db, email)

    if not client:
        raise HTTPException(
            status_code=404,
            detail="Client introuvable.",
        )

    return client


@router.get("/{client_id}")
def read_client(
    client_id: int,
    db: Session = Depends(get_db),
):
    try:
        return get_client(db, client_id)
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )


@router.patch("/{client_id}")
def update(
    client_id: int,
    client_data: ClientUpdate,
    db: Session = Depends(get_db),
):
    try:
        return update_client(db, client_id, client_data)

    except DuplicateEmailError as e:
        raise HTTPException(
            status_code=409,
            detail=str(e),
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.delete("/{client_id}")
def delete(
    client_id: int,
    db: Session = Depends(get_db),
):
    try:
        delete_client(db, client_id)
        return {"message": "Client supprimé avec succès."}
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )