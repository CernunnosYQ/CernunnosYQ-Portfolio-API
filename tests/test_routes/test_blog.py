from fastapi import status

from tests.utils import (
    create_random_test_user,
    create_random_test_blogpost,
    create_random_test_blogpost_list,
)

DATA = {"title": "Test title", "content": "", "is_active": True}


def test_create_blogpost(client, db_session):
    _, _, token = create_random_test_user(db_session)

    response = client.post(
        "/api/create/post", json=DATA, headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert set(response.json().keys()) == {
        "id",
        "title",
        "slug",
        "banner",
        "created_at",
        "content",
        "author",
        "is_active",
    }

    # Test post duplicated error
    assert (
        client.post(
            "/api/create/post", json=DATA, headers={"Authorization": f"Bearer {token}"}
        ).status_code
        == status.HTTP_409_CONFLICT
    )

    # Test unauthorized error
    assert (
        client.post("/api/create/post", json=DATA).status_code
        == status.HTTP_401_UNAUTHORIZED
    )


def test_get_all_posts(client, db_session):
    user, _, _ = create_random_test_user(db_session)
    blogpost_list = create_random_test_blogpost_list(
        author_id=user.id, db=db_session, quantity=5
    )
    response = client.get("/api/get/post/all")

    assert response.status_code == status.HTTP_200_OK

    # Test if it returns a list of posts and the correct number
    assert len(response.json()) == len(blogpost_list)
    for i in range(len(response.json())):
        # Test if every field is returned
        assert set(response.json()[i].keys()) == {
            "id",
            "title",
            "slug",
            "banner",
            "created_at",
            "content",
            "author",
            "is_active",
        }

        # Test if the response data matches with the given data
        assert response.json()[i]["author"] == user.username
        assert response.json()[i]["title"] == blogpost_list[i].title
        assert response.json()[i]["content"] == blogpost_list[i].content


def test_get_single_post(client, db_session):
    user, _, _ = create_random_test_user(db_session)
    blogpost = create_random_test_blogpost(user.id, db_session)

    # Test get blogpost by ID
    response_by_id = client.get(f"/api/get/post/by-id/{blogpost.id}")
    assert response_by_id.status_code == status.HTTP_200_OK

    # Test get blogpost by slug
    response_by_slug = client.get(f"/api/get/post/by-slug/{blogpost.slug}")
    assert response_by_slug.status_code == status.HTTP_200_OK

    # Compare the responses
    assert response_by_id.json() == response_by_slug.json()

    # Test not found error
    assert (
        client.get("/api/get/post/by-id/9999").status_code == status.HTTP_404_NOT_FOUND
    )
    assert (
        client.get("/api/get/post/by-slug/this-post-does-not-exists").status_code
        == status.HTTP_404_NOT_FOUND
    )


def test_update_post(client, db_session):
    user, _, token = create_random_test_user(db_session)

    blogpost = create_random_test_blogpost(user.id, db_session)
    old_data = blogpost.__dict__.copy()
    new_data = {
        "title": "New title for the post.",
        "content": "This is a new content for this post.",
    }

    response = client.put(
        f"/api/update/post/{blogpost.id}",
        json=new_data,
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_200_OK

    # Test data change
    assert response.json()["title"] != old_data["title"]
    assert response.json()["content"] != old_data["content"]

    # Test not found error
    assert (
        client.put(
            "/api/update/post/9999",
            json=new_data,
            headers={"Authorization": f"Bearer {token}"},
        ).status_code
        == status.HTTP_404_NOT_FOUND
    )

    # Test unauthorized error
    response_unauthorized = client.put(
        f"/api/update/post/{blogpost.id}",
        json=new_data,
        headers={"Authorization": "Bearer invalid_token"},
    )
    assert response_unauthorized.status_code == status.HTTP_401_UNAUTHORIZED

    # Test forbbiden error if trying to update another user's post
    _, _, other_user_token = create_random_test_user(db_session)
    response_forbidden = client.put(
        f"/api/update/post/{blogpost.id}",
        json=new_data,
        headers={"Authorization": f"Bearer {other_user_token}"},
    )
    assert response_forbidden.status_code == status.HTTP_403_FORBIDDEN


def test_delete_post(client, db_session):
    user, _, token = create_random_test_user(db_session)
    other_user, _, other_token = create_random_test_user(db_session)

    blogpost = create_random_test_blogpost(user.id, db_session)

    # Test unauthorized error when token os invalid, expired or None
    response_unauthorized = client.delete(f"/api/delete/post/{blogpost.id}")
    assert response_unauthorized.status_code == status.HTTP_401_UNAUTHORIZED

    # Test forbidden error when deleting someone else's post
    response_forbidden = client.delete(
        f"/api/delete/post/{blogpost.id}",
        headers={"Authorization": f"Bearer {other_token}"},
    )
    assert response_forbidden.status_code == status.HTTP_403_FORBIDDEN

    # Test not found error when deleting a non-existing post
    response_not_found = client.delete(
        "/api/delete/post/9999", headers={"Authorization": f"Bearer {token}"}
    )
    assert response_not_found.status_code == status.HTTP_404_NOT_FOUND

    # Test valid delete request
    response = client.delete(
        f"/api/delete/post/{blogpost.id}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK

    # Check that the post is deleted
    assert (
        client.get(f"/api/get/post/by-id/{blogpost.id}").status_code
        == status.HTTP_404_NOT_FOUND
    )
