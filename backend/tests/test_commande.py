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

def test_commande_livree_ne_peut_plus_changer_statut(api_client, headers):
    client_data = {
        "nom": "Client Livraison Test",
        "email": "livraison.test.20260902@example.com"
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

    # BROUILLON → CONFIRMÉE
    response = api_client.patch(
        f"/commandes/{commande['id']}/statut",
        json={"statut": "confirmée"},
        headers=headers
    )
    assert response.status_code == 200

    # CONFIRMÉE → EXPÉDIÉE
    response = api_client.patch(
        f"/commandes/{commande['id']}/statut",
        json={"statut": "expédiée"},
        headers=headers
    )
    assert response.status_code == 200

    # EXPÉDIÉE → LIVRÉE
    response = api_client.patch(
        f"/commandes/{commande['id']}/statut",
        json={"statut": "livrée"},
        headers=headers
    )
    assert response.status_code == 200

    # LIVRÉE → CONFIRMÉE : interdit
    response = api_client.patch(
        f"/commandes/{commande['id']}/statut",
        json={"statut": "confirmée"},
        headers=headers
    )

    assert response.status_code == 400

def test_list_commandes_pagination(api_client, headers):
    client_data = {
        "nom": "Client Pagination Test",
        "email": "pagination.test.20260902@example.com"
    }

    client_response = api_client.post(
        "/clients",
        json=client_data,
        headers=headers
    )

    assert client_response.status_code == 201
    client = client_response.json()

    # Création de 3 commandes
    for _ in range(3):
        response = api_client.post(
            "/commandes",
            json={"client_id": client["id"]},
            headers=headers
        )
        assert response.status_code == 201

    # Page 1 avec 2 éléments
    response = api_client.get(
        "/commandes?page=1&page_size=2",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data["items"]) == 2
    assert data["total"] >= 3
    assert data["page"] == 1
    assert data["page_size"] == 2

def test_list_commandes_filters(api_client, headers):
    client_data = {
        "nom": "Client Filtres Test",
        "email": "filtres.test.20260902@example.com"
    }

    client_response = api_client.post(
        "/clients",
        json=client_data,
        headers=headers
    )

    assert client_response.status_code == 201
    client = client_response.json()

    # Création de deux commandes pour ce client
    for _ in range(2):
        response = api_client.post(
            "/commandes",
            json={"client_id": client["id"]},
            headers=headers
        )
        assert response.status_code == 201

    # Filtre par client_id
    response = api_client.get(
        f"/commandes?client_id={client['id']}",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 2
    assert all(
        commande["client_id"] == client["id"]
        for commande in data["items"]
    )

    # Filtre par statut
    response = api_client.get(
        "/commandes?statut=brouillon",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert all(
        commande["statut"] == "brouillon"
        for commande in data["items"]
    )