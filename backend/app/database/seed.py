from datetime import datetime
from decimal import Decimal

from app.database.database import SessionLocal
from app.models.client import Client
from app.models.commande import Commande, StatutCommande
from app.models.ligne_commande import LigneCommande


def seed_database():
    db = SessionLocal()

    try:
        # Clients
        client1 = Client(
            nom="Alice Dupont",
            email="alice.dupont@example.com",
            date_creation=datetime.now()
        )

        client2 = Client(
            nom="Thomas Martin",
            email="thomas.martin@example.com",
            date_creation=datetime.now()
        )

        client3 = Client(
            nom="Sarah Bernard",
            email="sarah.bernard@example.com",
            date_creation=datetime.now()
        )

        db.add_all([client1, client2, client3])
        db.flush()

        # Commandes
        commande1 = Commande(
            client_id=client1.id,
            statut=StatutCommande.CONFIRMEE,
            date_commande=datetime.now(),
            montant_total=Decimal("59.98")
        )

        commande2 = Commande(
            client_id=client1.id,
            statut=StatutCommande.LIVREE,
            date_commande=datetime.now(),
            montant_total=Decimal("129.99")
        )

        commande3 = Commande(
            client_id=client2.id,
            statut=StatutCommande.BROUILLON,
            date_commande=datetime.now(),
            montant_total=Decimal("24.50")
        )

        commande4 = Commande(
            client_id=client3.id,
            statut=StatutCommande.EXPEDIEE,
            date_commande=datetime.now(),
            montant_total=Decimal("89.90")
        )

        db.add_all([commande1, commande2, commande3, commande4])
        db.flush()

        # Lignes de commande
        lignes = [
            LigneCommande(
                commande_id=commande1.id,
                reference_article="ART-001",
                libelle="T-shirt blanc",
                quantite=2,
                prix_unitaire=Decimal("29.99")
            ),
            LigneCommande(
                commande_id=commande2.id,
                reference_article="ART-002",
                libelle="Jean bleu",
                quantite=1,
                prix_unitaire=Decimal("79.99")
            ),
            LigneCommande(
                commande_id=commande2.id,
                reference_article="ART-003",
                libelle="Casquette noire",
                quantite=1,
                prix_unitaire=Decimal("50.00")
            ),
            LigneCommande(
                commande_id=commande3.id,
                reference_article="ART-004",
                libelle="Chaussettes blanches",
                quantite=1,
                prix_unitaire=Decimal("24.50")
            ),
            LigneCommande(
                commande_id=commande4.id,
                reference_article="ART-005",
                libelle="Sweat-shirt",
                quantite=2,
                prix_unitaire=Decimal("44.95")
            ),
        ]

        db.add_all(lignes)

        db.commit()

        print("Base de données remplie avec succès !")

    except Exception as e:
        db.rollback()
        print(f"Erreur : {e}")

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()