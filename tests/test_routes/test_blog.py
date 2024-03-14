def test_config(client):
    response = client.get("/api/get/post/all")
    print(response, response.json)
    assert response.status_code == 200
