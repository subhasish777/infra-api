from app import create_app


app = create_app()
client = app.test_client()


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert b"Welcome to Infra List of Servers" in response.data


def test_version():
    response = client.get("/version")

    assert response.status_code == 200
    assert b"ver 1.0.0" in response.data


def test_author():
    response = client.get("/author")

    assert response.status_code == 200
    assert b"current user" in response.data

def test_get_servers():
    response = client.get("/servers")

    assert response.status_code == 200

    data = response.get_json()

    assert isinstance(data, list)
    assert len(data) > 0

    first_server = data[0]

    assert "id" in first_server
    assert "name" in first_server
    assert "ip" in first_server
    assert "os" in first_server


def test_get_server_not_found():
    response = client.get("/servers/9999")

    assert response.status_code == 404

    data = response.get_json()

    assert data["error"] == "Server not found"


def test_create_server():

    payload = {
        "name": "test-server",
        "ip": "10.10.10.10",
        "os": "Ubuntu"
    }

    response = client.post("/servers", json=payload)

    assert response.status_code == 201

    data = response.get_json()

    assert data["message"] == "Server created successfully"
    assert "id" in data