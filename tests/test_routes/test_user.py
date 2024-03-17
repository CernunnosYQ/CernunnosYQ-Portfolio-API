from fastapi import status
from tests.utils import create_custom_test_user, create_default_test_user
from core.jwt_utils import validate_access_token


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

    assert create_user_response.status_code == status.HTTP_201_CREATED
    assert data["username"] == create_user_response.json()["username"]
    assert create_user_response.json().get("password") is None

    # Check user duplicated error
    client.post("api/create/user", json=data).status_code == status.HTTP_409_CONFLICT

    data["password2"] = "DontMach"

    # Check password dont match error
    assert (
        client.post("api/create/user", json=data).status_code
        == status.HTTP_400_BAD_REQUEST
    )

    data["password"] = "Unsecure"
    data["password2"] = "Unsecure"

    # Check password security error
    assert (
        client.post("api/create/user", json=data).status_code
        == status.HTTP_400_BAD_REQUEST
    )


def test_get_user(client, db_session):
    """
    Test create new user and retrieve its information.
    """

    create_custom_test_user(user_data=DATA, db=db_session)

    get_user_response = client.get(f"api/get/user/{DATA['username']}")
    assert get_user_response.status_code == status.HTTP_200_OK
    assert DATA["username"] == get_user_response.json()["username"]

    # Check user not found error
    assert (
        client.get("api/get/user/" + "NonExistentUser").status_code
        == status.HTTP_404_NOT_FOUND
    )


def test_update_password(client, db_session):
    """
    Test update password for a valid existing user.
    """

    user, token = create_custom_test_user(DATA, db=db_session)

    old_password = DATA["password"]
    new_password = "NewSecurePassword123!"

    update_user_response = client.put(
        f"/api/update/password/{user.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "old_password": old_password,
            "new_password": new_password,
            "new_password2": new_password,
        },
    )

    assert update_user_response.status_code == status.HTTP_200_OK


def test_delete_user(client, db_session):
    """
    Test delete user by id and check if the user is no longer in the database.
    """

    _, token = create_custom_test_user(DATA, db=db_session)

    response = client.delete(
        "/api/delete/user/1", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK


def test_login(client, db_session):
    create_custom_test_user(DATA, db=db_session)
    login_response = client.post(
        "/api/login", data={"username": DATA["username"], "password": DATA["password"]}
    )

    assert login_response.status_code == status.HTTP_200_OK

    login_data = login_response.json()
    assert "access_token" in login_data
    assert validate_access_token(login_data["access_token"]).get("success")
