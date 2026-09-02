from decimal import Decimal
from datetime import datetime

from app.database.database import SessionLocal
from app.models.client import Client
from app.models.commande import Commande, StatutCommande
from app.models.ligne_commande import LigneCommande


def seed():
    db = SessionLocal()

    try:
        if db.query(Client).first():
            print("La base contient déjà des données.")
            return

        # Clients
        client1 = Client(
            nom="Alice Martin",
            email="alice.martin@example.com"
        )

        client2 = Client(
            nom="Thomas Bernard",
            email="thomas.bernard@example.com"
        )

        client3 = Client(
            nom="Sophie Dubois",
            email="sophie.dubois@example.com"
        )

        db.add_all([client1, client2, client3])
        db.flush()

        # Commandes
        commande1 = Commande(
            client_id=client1.id,
            statut=StatutCommande.LIVREE,
            montant_total=Decimal("0.00")
        )

        commande2 = Commande(
            client_id=client1.id,
            statut=StatutCommande.CONFIRMEE,
            montant_total=Decimal("0.00")
        )

        commande3 = Commande(
            client_id=client2.id,
            statut=StatutCommande.EXPEDIEE,
            montant_total=Decimal("0.00")
        )

        commande4 = Commande(
            client_id=client3.id,
            statut=StatutCommande.BROUILLON,
            montant_total=Decimal("0.00")
        )

        db.add_all([
            commande1,
            commande2,
            commande3,
            commande4
        ])

        db.flush()

        # Lignes
        lignes = [
            LigneCommande(
                commande_id=commande1.id,
                reference_article="ART-001",
                libelle="Clavier mécanique",
                quantite=1,
                prix_unitaire=Decimal("39.99")
            ),
            LigneCommande(
                commande_id=commande1.id,
                reference_article="ART-002",
                libelle="Souris sans fil",
                quantite=1,
                prix_unitaire=Decimal("19.98")
            ),
            LigneCommande(
                commande_id=commande2.id,
                reference_article="ART-003",
                libelle="Écran 24 pouces",
                quantite=1,
                prix_unitaire=Decimal("120.00")
            ),
            LigneCommande(
                commande_id=commande3.id,
                reference_article="ART-004",
                libelle="Casque audio",
                quantite=1,
                prix_unitaire=Decimal("45.50")
            )
        ]

        db.add_all(lignes)
        db.flush()

        # Recalcul des totaux
        commande1.montant_total = sum(
            (ligne.quantite * ligne.prix_unitaire
             for ligne in commande1.lignes),
            Decimal("0.00")
        )

        commande2.montant_total = sum(
            (ligne.quantite * ligne.prix_unitaire
             for ligne in commande2.lignes),
            Decimal("0.00")
        )

        commande3.montant_total = sum(
            (ligne.quantite * ligne.prix_unitaire
             for ligne in commande3.lignes),
            Decimal("0.00")
        )

        db.commit()

        print("Seed exécuté avec succès.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed()