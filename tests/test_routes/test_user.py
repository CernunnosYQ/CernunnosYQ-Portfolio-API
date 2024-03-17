from fastapi import status
from tests.utils import create_custom_test_user, create_default_test_user


DATA = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "Password123!",
    "password2": "Password123!",
}


def test_create_user(client):
    """
    Tests that a new user can be created and returned in the response body as JSON.
    """

    data = DATA.copy()

    create_user_response = client.post("api/create/user", json=data)
    duplicate_user_response = client.post("api/create/user", json=data)

    data["password2"] = "DontMach"

    assert (
        client.post("api/create/user", json=data).status_code
        == status.HTTP_400_BAD_REQUEST
    )

    data["password"] = "Unsecure"
    data["password2"] = "Unsecure"

    assert (
        client.post("api/create/user", json=data).status_code
        == status.HTTP_400_BAD_REQUEST
    )

    assert create_user_response.status_code == status.HTTP_201_CREATED
    assert data["username"] == create_user_response.json()["username"]
    assert create_user_response.json().get("password") is None
    assert duplicate_user_response.status_code == status.HTTP_409_CONFLICT


def test_get_user(client, db_session):
    """
    Test create new user and retrieve its information.
    """

    data = DATA.copy()

    create_custom_test_user(user_data=data, db=db_session)

    assert (
        client.get("api/get/user/" + "NonExistentUser").status_code
        == status.HTTP_404_NOT_FOUND
    )

    get_user_response = client.get(f"api/get/user/{data['username']}")
    assert get_user_response.status_code == status.HTTP_200_OK
    assert data["username"] == get_user_response.json()["username"]


def test_update_user(client, db_session):
    pass


def test_delete_user(client, db_session):
    pass


def test_login(client):
    pass
