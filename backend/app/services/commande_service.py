from datetime import datetime
from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.client import Client
from app.models.commande import Commande, StatutCommande
from app.schemas.commande import CommandeCreate, CommandeUpdate

import logging

logger = logging.getLogger(__name__)

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

    logger.info(
    "Création d'une commande pour le client %s",
    commande_data.client_id,
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

def get_commandes(
    db: Session,
    client_id: int | None = None,
    statut: StatutCommande | None = None,
    montant_min: Decimal | None = None,
    montant_max: Decimal | None = None,
    page: int = 1,
    page_size: int = 10,
):
    query = db.query(Commande)

    if client_id is not None:
        query = query.filter(Commande.client_id == client_id)

    if statut is not None:
        query = query.filter(Commande.statut == statut)

    if montant_min is not None:
        query = query.filter(Commande.montant_total >= montant_min)

    if montant_max is not None:
        query = query.filter(Commande.montant_total <= montant_max)

    total = query.count()

    offset = (page - 1) * page_size

    commandes = (
        query
        .offset(offset)
        .limit(page_size)
        .all()
    )

    return commandes, total

def update_commande(
    db: Session,
    commande_id: int,
    commande_data: CommandeUpdate,
):
    commande = get_commande(db, commande_id)

    if commande_data.statut is not None:
        nouveau_statut = commande_data.statut

        if nouveau_statut not in TRANSITIONS_AUTORISEES[commande.statut]:
            logger.warning(
                "Transition de statut non autorisée pour la commande %s : %s → %s",
                commande_id,
                commande.statut,
                nouveau_statut,
            )   
            raise ValueError(
                f"Transition impossible : "
                f"{commande.statut} → {nouveau_statut}"
            )
        
        logger.info(
            "Mise à jour du statut de la commande %s de %s à %s",
            commande_id,
            commande.statut,
            nouveau_statut,
            )
        
        commande.statut = nouveau_statut

    db.commit()
    db.refresh(commande)

    return commande