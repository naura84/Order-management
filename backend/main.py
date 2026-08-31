from fastapi import APIRouter, FastAPI
from app.routes.client_routes import router as client_router
from app.routes.commandes_routes import router as commande_router
from app.routes.ligne_commande_routes import router as ligne_commande_router
from app.routes.stat_routes import router as stat_router

from app.utils.logging_config import setup_logging


setup_logging()

app = FastAPI()

app.include_router(client_router)
app.include_router(commande_router)
app.include_router(ligne_commande_router)
app.include_router(stat_router)