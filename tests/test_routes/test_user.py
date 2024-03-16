from fastapi import status


data = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "Password123!",
    "password2": "Password123!",
}


def test_new_user(client):
    """
    Test create new user and retrieve its information.
    """

    create_user_response = client.post("api/create/user", json=data)

    assert create_user_response.status_code == status.HTTP_201_CREATED
    assert data["username"] in create_user_response.json()["username"]
    assert create_user_response.json().get("password") is None

    get_user_response = client.get(f"api/get/user/{data['username']}")
    assert get_user_response.status_code == status.HTTP_200_OK
    assert data["username"] == get_user_response.json()["username"]
    print(get_user_response.json())
    print(get_user_response.json().get("email") or "No email provided.")
