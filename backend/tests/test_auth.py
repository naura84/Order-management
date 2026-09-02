def test_auth_missing_api_key(api_client):
    response = api_client.get("/commandes")

    assert response.status_code == 401


def test_auth_invalid_api_key(api_client):
    response = api_client.get(
        "/commandes",
        headers={"X-API-Key": "wrong-api-key"}
    )

    assert response.status_code == 401


def test_auth_valid_api_key(api_client, headers):
    response = api_client.get(
        "/commandes",
        headers=headers
    )

    assert response.status_code == 200