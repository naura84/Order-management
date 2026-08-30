from datetime import datetime
from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.client import Client
from app.models.commande import Commande, StatutCommande
from app.schemas.commande import CommandeCreate, CommandeUpdate

# List of allowed status transitions for a Commande
TRANSITIONS_AUTORISEES = {
    StatutCommande.BROUILLON: {
        StatutCommande.CONFIRMEE,
        StatutCommande.ANNULEE,
    },
    StatutCommande.CONFIRMEE: {
        StatutCommande.EXPEDIEE,
        StatutCommande.ANNULEE,
    },
    StatutCommande.EXPEDIEE: {
        StatutCommande.LIVREE,
    },
    StatutCommande.LIVREE: set(),
    StatutCommande.ANNULEE: set(),
}

def create_commande(db: Session, commande_data: CommandeCreate):
    client = (
        db.query(Client)
        .filter(Client.id == commande_data.client_id)
        .first()
    )

    if not client:
        raise ValueError("Client introuvable.")

    commande = Commande(
        client_id=commande_data.client_id,
        statut=StatutCommande.BROUILLON,
        date_commande=datetime.utcnow(),
        montant_total=Decimal("0.00"),
    )

    db.add(commande)
    db.commit()
    db.refresh(commande)

    return commande

def get_commande(db: Session, commande_id: int):
    commande = (
        db.query(Commande)
        .filter(Commande.id == commande_id)
        .first()
    )

    if not commande:
        raise ValueError("Commande introuvable.")

    return commande

def get_commandes(db: Session):
    return db.query(Commande).all()

def update_commande(
    db: Session,
    commande_id: int,
    commande_data: CommandeUpdate,
):
    commande = get_commande(db, commande_id)

    if commande_data.statut is not None:
        nouveau_statut = commande_data.statut

        if nouveau_statut not in TRANSITIONS_AUTORISEES[commande.statut]:
            raise ValueError(
                f"Transition impossible : "
                f"{commande.statut} → {nouveau_statut}"
            )

        commande.statut = nouveau_statut

    db.commit()
    db.refresh(commande)

    return commande