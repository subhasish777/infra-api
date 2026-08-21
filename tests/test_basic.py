import uuid
from app import create_app

app = create_app()
client = app.test_client()

# ==========================================
# STATIC ROUTES
# ==========================================

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    # Changed to match the new HTML dashboard
    assert b"Infrastructure API Dashboard" in response.data

def test_version():
    response = client.get("/version")
    assert response.status_code == 200
    assert b"ver 1.0.0" in response.data

def test_author():
    response = client.get("/author")
    assert response.status_code == 200
    assert b"current user" in response.data

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"

# ==========================================
# SERVER API ROUTES
# ==========================================

def test_get_servers():
    response = client.get("/servers")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    # Removed len(data) > 0 so it passes on empty databases

def test_get_server_not_found():
    response = client.get("/servers/999999")
    assert response.status_code == 404
    data = response.get_json()
    assert data["error"] == "Server not found"

def test_crud_lifecycle():
    """
    Tests POST, GET by ID, PUT, PATCH, and DELETE in a single 
    lifecycle to ensure they all work together without leaving junk data.
    """
    # 1. Generate unique data to bypass Postgres UNIQUE constraints
    unique_suffix = str(uuid.uuid4())[:8]
    payload = {
        "name": f"test-server-{unique_suffix}",
        "ip": f"10.0.0.{uuid.uuid4().int % 255}",
        "os": "Ubuntu"
    }

    # 2. Test POST
    post_resp = client.post("/servers", json=payload)
    assert post_resp.status_code == 201
    post_data = post_resp.get_json()
    assert post_data["message"] == "Server created successfully"
    server_id = post_data["id"]

    # 3. Test GET by ID
    get_resp = client.get(f"/servers/{server_id}")
    assert get_resp.status_code == 200
    assert get_resp.get_json()["name"] == payload["name"]

    # 4. Test PUT
    put_payload = {
        "name": f"updated-{unique_suffix}",
        "ip": payload["ip"],
        "os": "RHEL"
    }
    put_resp = client.put(f"/servers/{server_id}", json=put_payload)
    assert put_resp.status_code == 200

    # 5. Test PATCH
    patch_resp = client.patch(f"/servers/{server_id}", json={"os": "Debian"})
    assert patch_resp.status_code == 200

    # 6. Test DELETE
    del_resp = client.delete(f"/servers/{server_id}")
    assert del_resp.status_code == 200

    # 7. Verify DELETED
    verify_resp = client.get(f"/servers/{server_id}")
    assert verify_resp.status_code == 404

# ==========================================
# VALIDATION TESTS
# ==========================================

def test_post_validation_error():
    # Test name length validation (must be > 3 chars)
    payload = {
        "name": "web", 
        "ip": "1.1.1.1",
        "os": "Ubuntu"
    }
    response = client.post("/servers", json=payload)
    assert response.status_code == 400
    assert b"Server name should be more than 3 char" in response.data