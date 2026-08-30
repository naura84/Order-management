from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class LigneCommandeCreate(BaseModel):
    reference_article: str
    libelle: str
    quantite: int = Field(gt=0)
    prix_unitaire: Decimal = Field(gt=0)


class LigneCommandeUpdate(BaseModel):
    quantite: int | None = Field(default=None, gt=0)


class LigneCommandeResponse(BaseModel):
    id: int
    commande_id: int
    reference_article: str
    libelle: str
    quantite: int
    prix_unitaire: Decimal

    model_config = ConfigDict(from_attributes=True)