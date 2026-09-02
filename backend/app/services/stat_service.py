from collections import Counter
from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.client import Client
from app.models.commande import Commande


def get_stats_client(
    db: Session,
    client_id: int,
):
    client = (
        db.query(Client)
        .filter(Client.id == client_id)
        .first()
    )

    if not client:
        raise ValueError("Client introuvable.")

    commandes = (
        db.query(Commande)
        .filter(Commande.client_id == client_id)
        .all()
    )

    nombre_commandes = len(commandes)

    montant_total = sum(
        (commande.montant_total for commande in commandes),
        Decimal("0.00"),
    )

    panier_moyen = (
        montant_total / nombre_commandes
        if nombre_commandes > 0
        else Decimal("0.00")
    )

    statuts = Counter(
        commande.statut.value
        for commande in commandes
    )

    statut_plus_frequent = (
        statuts.most_common(1)[0][0]
        if statuts
        else None
    )

    return {
        "nombre_commandes": nombre_commandes,
        "montant_total": montant_total,
        "panier_moyen": panier_moyen,
        "statut_plus_frequent": statut_plus_frequent,
    }