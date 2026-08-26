from datetime import datetime
from decimal import Decimal
from enum import Enum

from sqlalchemy import DateTime, Enum as SAEnum, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base


class StatutCommande(str, Enum):
    BROUILLON = "brouillon"
    CONFIRMEE = "confirmée"
    EXPEDIEE = "expédiée"
    LIVREE = "livrée"
    ANNULEE = "annulée"


class Commande(Base):
    __tablename__ = "commandes"

    id: Mapped[int] = mapped_column(primary_key=True)

    client_id: Mapped[int] = mapped_column(
        ForeignKey("clients.id"),
        nullable=False,
    )

    statut: Mapped[StatutCommande] = mapped_column(
        SAEnum(StatutCommande),
        default=StatutCommande.BROUILLON,
        nullable=False,
    )

    date_commande: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    montant_total: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        default=Decimal("0.00"),
        nullable=False,
    )

    client = relationship(
        "Client",
        back_populates="commandes",
    )

    lignes = relationship(
        "LigneCommande",
        back_populates="commande",
        cascade="all, delete-orphan",
    )