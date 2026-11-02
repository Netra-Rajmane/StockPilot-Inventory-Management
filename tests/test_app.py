import os
import tempfile
import pytest
from app import app, init_db

@pytest.fixture()
def client():
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "test"
    import app as app_module
    original = app_module.DB_PATH
    app_module.DB_PATH = path
    init_db()
    with app.test_client() as client:
        yield client
    app_module.DB_PATH = original
    os.unlink(path)

def test_home_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Inventory" in response.data

def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"

def test_products_api_returns_seed_data(client):
    response = client.get("/api/products")
    assert response.status_code == 200
    assert len(response.get_json()) >= 1

def test_add_product(client):
    response = client.post("/products/add", data={
        "name": "Test Monitor", "sku": "TEST-001", "category": "Electronics",
        "quantity": "12", "price": "4500", "supplier": "Test Supplier"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Test Monitor" in response.data

def test_reject_duplicate_sku(client):
    client.post("/products/add", data={
        "name": "One", "sku": "DUP-1", "category": "Other",
        "quantity": "1", "price": "10", "supplier": ""
    })
    response = client.post("/products/add", data={
        "name": "Two", "sku": "DUP-1", "category": "Other",
        "quantity": "1", "price": "10", "supplier": ""
    }, follow_redirects=True)
    assert b"SKU already exists" in response.data
