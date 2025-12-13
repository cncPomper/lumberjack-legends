def test_signup(client):
    response = client.post("/api/auth/signup", json={
        "username": "NewUser",
        "email": "new@user.com",
        "password": "password123"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["success"] == True
    assert data["user"]["username"] == "NewUser"
    assert "token" in data

def test_login(client):
    response = client.post("/api/auth/login", json={
        "email": "king@forest.com",
        "password": "password"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert "token" in data

def test_get_me(client, auth_token):
    response = client.get("/api/auth/me", headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert data["user"]["email"] == "king@forest.com"
