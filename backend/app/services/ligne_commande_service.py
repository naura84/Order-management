from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.commande import Commande, StatutCommande
from app.models.ligne_commande import LigneCommande
from app.schemas.ligne_commande import LigneCommandeCreate, LigneCommandeUpdate

def check_commande_modifiable(commande: Commande):
    if commande.statut in {
        StatutCommande.LIVREE,
        StatutCommande.ANNULEE,
    }:
        raise ValueError(
            "Impossible de modifier une commande terminée."
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

    if check_commande_modifiable(commande):
        raise ValueError(
            "Impossible de modifier une commande terminée."
        )

    ligne = LigneCommande(
        commande_id=commande_id,
        reference_article=ligne_data.reference_article,
        libelle=ligne_data.libelle,
        quantite=ligne_data.quantite,
        prix_unitaire=ligne_data.prix_unitaire,
    )

    db.add(ligne)
    db.commit()
    db.refresh(ligne)

    return ligne

def recalculate_total(db: Session, commande: Commande):
    total = sum(
        (
            ligne.quantite * ligne.prix_unitaire
            for ligne in commande.lignes
        ),
        Decimal("0.00"),
    )

    commande.montant_total = total

    db.commit()
    db.refresh(commande)

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

    if check_commande_modifiable(commande):
        raise ValueError(
            "Impossible de modifier une commande terminée."
        )

    if ligne_data.quantite is not None:
        ligne.quantite = ligne_data.quantite

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

    if check_commande_modifiable(commande):
        raise ValueError(
            "Impossible de modifier une commande terminée."
        )

    db.delete(ligne)
    db.commit()