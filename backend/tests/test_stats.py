def test_client_stats(api_client, headers):
    client_data = {
        "nom": "Client Stats Test",
        "email": "stats.tet.20260902@example.com"
    }

    client_response = api_client.post(
        "/clients",
        json=client_data,
        headers=headers
    )

    assert client_response.status_code == 201
    client = client_response.json()

    # Création de 2 commandes
    for _ in range(2):
        response = api_client.post(
            "/commandes",
            json={"client_id": client["id"]},
            headers=headers
        )
        assert response.status_code == 201

    response = api_client.get(
        f"/stats/clients/{client['id']}",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["nombre_commandes"] == 2
    assert data["montant_total"] == "0.00"
    assert data["panier_moyen"] == "0.00"
    assert data["statut_plus_frequent"] == "brouillon"