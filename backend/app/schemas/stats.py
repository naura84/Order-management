from decimal import Decimal

from pydantic import BaseModel


class ClientStatsResponse(BaseModel):
    nombre_commandes: int
    montant_total: Decimal
    panier_moyen: Decimal
    statut_plus_frequent: str | None