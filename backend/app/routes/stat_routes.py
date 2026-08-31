from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.services.stat_service import get_stats_commandes


router = APIRouter(
    prefix="/stats",
    tags=["Statistiques"],
)


@router.get("/commandes")
def stats_commandes(
    db: Session = Depends(get_db),
):
    return get_stats_commandes(db)