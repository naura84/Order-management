from decimal import Decimal

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.commande import Commande, StatutCommande


def get_stats_commandes(db: Session):
    nombre_commandes = (
        db.query(func.count(Commande.id))
        .scalar()
    )

    chiffre_affaires = (
    db.query(func.sum(Commande.montant_total))
    .scalar()
    or Decimal("0.00")
    )
    
    chiffre_affaires = chiffre_affaires.quantize(Decimal("0.01"))

    montant_moyen = (
    db.query(func.avg(Commande.montant_total))
    .scalar()
    or Decimal("0.00")
    )
    
    montant_moyen = montant_moyen.quantize(Decimal("0.01"))

    commandes_par_statut = {}

    for statut in StatutCommande:
        nombre = (
            db.query(func.count(Commande.id))
            .filter(Commande.statut == statut)
            .scalar()
        )

        commandes_par_statut[statut.value] = nombre

    return {
        "nombre_commandes": nombre_commandes,
        "chiffre_affaires": chiffre_affaires,
        "montant_moyen": montant_moyen,
        "commandes_par_statut": commandes_par_statut,
    }