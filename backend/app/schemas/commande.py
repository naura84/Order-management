from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.models.commande import StatutCommande


class CommandeCreate(BaseModel):
    client_id: int

class CommandeUpdate(BaseModel):
    statut: StatutCommande | None = None

class CommandeResponse(BaseModel):
    id: int
    client_id: int
    statut: StatutCommande
    date_commande: datetime
    montant_total: Decimal

    model_config = ConfigDict(from_attributes=True)