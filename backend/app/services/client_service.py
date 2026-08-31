from sqlalchemy.orm import Session

from app.models.client import Client
from app.schemas.client import ClientCreate
from app.schemas.client import ClientCreate, ClientUpdate

import logging

logger = logging.getLogger(__name__)

def create_client(db: Session, client_data: ClientCreate):
    existing_client = (
        db.query(Client)
        .filter(Client.email == client_data.email)
        .first()
    )

    if existing_client:
        raise ValueError("Un client avec cet email existe déjà.")

    client = Client(
        nom=client_data.nom,
        email=client_data.email,
    )

    logger.info(
    "Création d'un client avec l'email %s",
    client_data.email,
    )

    db.add(client)
    db.commit()
    db.refresh(client)

    return client

def get_client(db: Session, client_id: int):
    client = db.query(Client).filter(Client.id == client_id).first()

    if not client:
        raise ValueError("Client introuvable.")

    return client

def get_clients(db: Session):
    return db.query(Client).all()

def get_client_by_email(db: Session, email: str):
    return db.query(Client).filter(Client.email == email).first()

def update_client(db: Session, client_id: int, client_data: ClientUpdate):
    client = get_client(db, client_id)

    if client_data.nom is not None:
        client.nom = client_data.nom

    if client_data.email is not None:
        existing_client = (
            db.query(Client)
            .filter(
                Client.email == client_data.email,
                Client.id != client_id,
            ) # This ensures that we don't consider the current client when checking for existing emails
            .first()
        )

        if existing_client:
            raise ValueError("Un client avec cet email existe déjà.")

        client.email = client_data.email
    
    logger.info(
    "Mise à jour du client %s",
    client_id,
    )

    db.commit()
    db.refresh(client)

    return client

# Temporary function to delete a client, ensuring that clients with existing orders cannot be deleted. This is a safeguard to maintain data integrity.
# Upgrade : deactivate the client instead of deleting it. This is a temporary solution to prevent data loss and maintain the integrity of the database. In the future, we will implement a more robust solution that allows for proper handling of client deletions while preserving historical data.
def delete_client(db: Session, client_id: int):
    client = get_client(db, client_id)

    if client.commandes:
        raise ValueError(
            "Impossible de supprimer un client ayant des commandes."
        )

    db.delete(client)
    db.commit()