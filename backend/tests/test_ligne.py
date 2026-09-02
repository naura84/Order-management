def test_add_ligne_commande_non_brouillon(api_client, headers):
    client_data = {
        "nom": "Client Ligne Statut Test",
        "email": "ligne.staut.test.20260902.v2@example.com"
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

def test_add_ligne_recalculate_total(api_client, headers):
    # Création d'un client
    client_data = {
        "nom": "Client Ligne Test",
        "email": "ligne.test.2260902.v2@example.com"
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

def test_add_ligne_quantite_invalide(api_client, headers):
    client_response = api_client.post(
        "/clients",
        json={
            "nom": "Client Quantite",
            "email": "quantite.tst@example.com"
        },
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

    response = api_client.post(
        f"/commandes/{commande['id']}/lignes",
        json={
            "reference_article": "ART-003",
            "libelle": "Quantité invalide",
            "quantite": 0,
            "prix_unitaire": 10.00
        },
        headers=headers
    )

    assert response.status_code == 422


def test_add_ligne_prix_invalide(api_client, headers):
    client_response = api_client.post(
        "/clients",
        json={
            "nom": "Client Prix",
            "email": "prix.test@eample.com"
        },
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

    response = api_client.post(
        f"/commandes/{commande['id']}/lignes",
        json={
            "reference_article": "ART-004",
            "libelle": "Prix invalide",
            "quantite": 1,
            "prix_unitaire": -5.00
        },
        headers=headers
    )

    assert response.status_code == 422