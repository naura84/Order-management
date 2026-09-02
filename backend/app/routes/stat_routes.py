from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth import verify_api_key
from app.database.database import get_db
from app.schemas.stats import ClientStatsResponse
from app.services.stat_service import get_stats_client


router = APIRouter(
    prefix="/stats",
    tags=["Statistiques"],
    dependencies=[Depends(verify_api_key)],
)


@router.get(
    "/clients/{client_id}",
    response_model=ClientStatsResponse,
)
def stats_client(
    client_id: int,
    db: Session = Depends(get_db),
):
    try:
        return get_stats_client(db, client_id)
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )