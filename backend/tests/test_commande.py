def test_create_commande(api_client, headers):
    # Création d'un client pour la commande
    client_data = {
        "nom": "Client Commande Test",
        "email": "commande.test.20260901.v3@example.com"
    }

    client_response = api_client.post(
        "/clients",
        json=client_data,
        headers=headers
    )

    assert client_response.status_code == 201

    client = client_response.json()

    # Création de la commande
    commande_data = {
        "client_id": client["id"]
    }

    response = api_client.post(
        "/commandes",
        json=commande_data,
        headers=headers
    )

    assert response.status_code == 201

    commande = response.json()

    assert commande["client_id"] == client["id"]
    assert commande["statut"] == "brouillon"
    assert commande["montant_total"] == 0.0

def test_add_ligne_recalculate_total(api_client, headers):
    # Création d'un client
    client_data = {
        "nom": "Client Ligne Test",
        "email": "ligne.test.20260901.v4@example.com"
    }

    client_response = api_client.post(
        "/clients",
        json=client_data,
        headers=headers
    )

    assert client_response.status_code == 201

    client = client_response.json()

    # Création d'une commande
    commande_response = api_client.post(
        "/commandes",
        json={
            "client_id": client["id"]
        },
        headers=headers
    )

    assert commande_response.status_code == 201

    commande = commande_response.json()

    # Ajout d'une ligne
    ligne_data = {
        "reference_article": "ART-001",
        "libelle": "Produit test",
        "quantite": 2,
        "prix_unitaire": 15.50
    }

    ligne_response = api_client.post(
        f"/commandes/{commande['id']}/lignes",
        json=ligne_data,
        headers=headers
    )

    assert ligne_response.status_code == 201

    # Vérification du montant recalculé
    commande_response = api_client.get(
        f"/commandes/{commande['id']}",
        headers=headers
    )

    assert commande_response.status_code == 200

    commande = commande_response.json()

    assert commande["montant_total"] == 31.0

def test_update_commande_statut(api_client, headers):
    # Création d'un client
    client_data = {
        "nom": "Client Statut Test",
        "email": "statut.tes.20260902@example.com"
    }

    client_response = api_client.post(
        "/clients",
        json=client_data,
        headers=headers
    )

    assert client_response.status_code == 201
    client = client_response.json()

    # Création d'une commande
    commande_response = api_client.post(
        "/commandes",
        json={"client_id": client["id"]},
        headers=headers
    )

    assert commande_response.status_code == 201
    commande = commande_response.json()

    # BROUILLON → CONFIRMÉE
    response = api_client.patch(
        f"/commandes/{commande['id']}/statut",
        json={"statut": "confirmée"},
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["statut"] == "confirmée"

def test_transition_statut_invalide(api_client, headers):
    client_data = {
        "nom": "Client Transition Test",
        "email": "transition.test.20260902@example.com"
    }

    client_response = api_client.post(
        "/clients",
        json=client_data,
        headers=headers
    )

    assert client_response.status_code == 201
    client = client_response.json()

    commande_response = api_client.post(
        "/commandes",
        json={"client_id": client["id"]},
        headers=headers
    )

    assert commande_response.status_code == 201
    commande = commande_response.json()

    # BROUILLON → LIVRÉE : transition interdite
    response = api_client.patch(
        f"/commandes/{commande['id']}/statut",
        json={"statut": "livrée"},
        headers=headers
    )

    assert response.status_code == 400

def test_add_ligne_commande_non_brouillon(api_client, headers):
    client_data = {
        "nom": "Client Ligne Statut Test",
        "email": "ligne.statut.test.20260902@example.com"
    }

    client_response = api_client.post(
        "/clients",
        json=client_data,
        headers=headers
    )

    assert client_response.status_code == 201
    client = client_response.json()

    commande_response = api_client.post(
        "/commandes",
        json={"client_id": client["id"]},
        headers=headers
    )

    assert commande_response.status_code == 201
    commande = commande_response.json()

    # Passage de BROUILLON à CONFIRMÉE
    statut_response = api_client.patch(
        f"/commandes/{commande['id']}/statut",
        json={"statut": "confirmée"},
        headers=headers
    )

    assert statut_response.status_code == 200

    # Tentative d'ajout d'une ligne sur une commande confirmée
    ligne_response = api_client.post(
        f"/commandes/{commande['id']}/lignes",
        json={
            "reference_article": "ART-002",
            "libelle": "Produit interdit",
            "quantite": 1,
            "prix_unitaire": 10.00
        },
        headers=headers
    )

    assert ligne_response.status_code == 400