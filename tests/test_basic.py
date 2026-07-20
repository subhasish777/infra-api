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