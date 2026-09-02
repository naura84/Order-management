from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.commande import Commande, StatutCommande
from app.models.ligne_commande import LigneCommande
from app.schemas.ligne_commande import LigneCommandeCreate, LigneCommandeUpdate

import logging

logger = logging.getLogger(__name__)


def check_commande_modifiable(commande: Commande):
    if commande.statut != StatutCommande.BROUILLON:
        raise ValueError(
            "Impossible de modifier une commande qui n'est pas en brouillon."
        )

def recalculate_total(db: Session, commande: Commande):
    total = sum(
        (
            ligne.quantite * ligne.prix_unitaire
            for ligne in commande.lignes
        ),
        Decimal("0.00"),
    )

    commande.montant_total = total

def get_lignes_commande(
    db: Session,
    commande_id: int,
):
    commande = (
        db.query(Commande)
        .filter(Commande.id == commande_id)
        .first()
    )

    if not commande:
        raise ValueError("Commande introuvable.")

    return (
        db.query(LigneCommande)
        .filter(LigneCommande.commande_id == commande_id)
        .all()
    )

def add_ligne(
    db: Session,
    commande_id: int,
    ligne_data: LigneCommandeCreate,
):
    commande = (
        db.query(Commande)
        .filter(Commande.id == commande_id)
        .first()
    )

    if not commande:
        raise ValueError("Commande introuvable.")

    check_commande_modifiable(commande)

    ligne = LigneCommande(
        commande_id=commande_id,
        reference_article=ligne_data.reference_article,
        libelle=ligne_data.libelle,
        quantite=ligne_data.quantite,
        prix_unitaire=ligne_data.prix_unitaire,
    )

    commande.lignes.append(ligne)

    recalculate_total(db, commande)

    logger.info(
    "Ajout d'une ligne de commande à la commande %s",
    commande_id,
    )

    db.commit()
    db.refresh(ligne)

    return ligne


def update_ligne(
    db: Session,
    ligne_id: int,
    ligne_data: LigneCommandeUpdate,
):
    ligne = (
        db.query(LigneCommande)
        .filter(LigneCommande.id == ligne_id)
        .first()
    )

    if not ligne:
        raise ValueError("Ligne de commande introuvable.")

    commande = (
        db.query(Commande)
        .filter(Commande.id == ligne.commande_id)
        .first()
    )

    if not commande:
        raise ValueError("Commande introuvable.")

    check_commande_modifiable(commande)

    if ligne_data.quantite is not None:
        ligne.quantite = ligne_data.quantite

    logger.info(
    "Mise à jour de la ligne de commande %s",
    ligne_id,
    )

    recalculate_total(db, commande)
    db.commit()
    db.refresh(ligne)

    return ligne

def delete_ligne(db: Session, ligne_id: int):
    ligne = (
        db.query(LigneCommande)
        .filter(LigneCommande.id == ligne_id)
        .first()
    )

    if not ligne:
        raise ValueError("Ligne de commande introuvable.")

    commande = (
        db.query(Commande)
        .filter(Commande.id == ligne.commande_id)
        .first()
    )

    if not commande:
        raise ValueError("Commande introuvable.")

    check_commande_modifiable(commande)

    logger.info(
    "Suppression de la ligne de commande %s",
    ligne_id,
    )
    
    db.delete(ligne)
    db.flush()

    recalculate_total(db, commande)

    db.commit()