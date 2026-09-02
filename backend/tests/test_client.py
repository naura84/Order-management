def test_create_client(api_client, headers):
    response = api_client.post(
        "/clients",
        json={
            "nom": "Test Client",
            "email": "tests.client.2026@example.com"
        },
        headers=headers
    )

    assert response.status_code == 201

    data = response.json()

    assert data["nom"] == "Test Client"
    assert data["email"] == "tests.client.2026@example.com"

def test_create_client_duplicate_email(api_client, headers):
    client_data = {
        "nom": "Client Doublon",
        "email": "duplicate.test.20260901@example.com"
    }

    first_response = api_client.post(
        "/clients",
        json=client_data,
        headers=headers
    )

    assert first_response.status_code == 201

    second_response = api_client.post(
        "/clients",
        json=client_data,
        headers=headers
    )

    assert second_response.status_code == 409