from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base


class LigneCommande(Base):
    __tablename__ = "lignes_commande"

    id: Mapped[int] = mapped_column(primary_key=True)

    commande_id: Mapped[int] = mapped_column(
        ForeignKey("commandes.id"),
        nullable=False,
    )

    reference_article: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    libelle: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    quantite: Mapped[int] = mapped_column(
        nullable=False,
    )

    prix_unitaire: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    commande = relationship(
        "Commande",
        back_populates="lignes",
    )