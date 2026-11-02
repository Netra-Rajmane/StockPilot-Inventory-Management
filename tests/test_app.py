
import os
import tempfile
import pytest

from app import app, init_db


@pytest.fixture()
def client():

    # Create temporary database
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)

    import app as app_module

    # Save original application settings
    original_db_path = app_module.DB_PATH
    original_testing = app.config.get("TESTING")
    original_secret = app.config.get("SECRET_KEY")

    # Configure test database
    app_module.DB_PATH = path
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "test"

    try:

        # Initialize temporary database
        init_db()

        with app.test_client() as test_client:
            yield test_client

    finally:

        # Restore original configuration
        app_module.DB_PATH = original_db_path
        app.config["TESTING"] = original_testing
        app.config["SECRET_KEY"] = original_secret

        # Delete temporary database
        if os.path.exists(path):
            os.unlink(path)


# Test 1: Home page
def test_home_page_loads(client):

    response = client.get("/")

    assert response.status_code == 200
    assert b"Inventory" in response.data


# Test 2: Health API
def test_health_endpoint(client):

    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


# Test 3: Products API
def test_products_api_returns_seed_data(client):

    response = client.get("/api/products")

    assert response.status_code == 200
    assert len(response.get_json()) >= 1


# Test 4: Add product
def test_add_product(client):

    response = client.post(
        "/products/add",
        data={
            "name": "Test Monitor",
            "sku": "TEST-001",
            "category": "Electronics",
            "quantity": "12",
            "price": "4500",
            "supplier": "Test Supplier"
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Test Monitor" in response.data


# Test 5: Reject duplicate SKU
def test_reject_duplicate_sku(client):

    client.post(
        "/products/add",
        data={
            "name": "One",
            "sku": "DUP-1",
            "category": "Other",
            "quantity": "1",
            "price": "10",
            "supplier": ""
        }
    )

    response = client.post(
        "/products/add",
        data={
            "name": "Two",
            "sku": "DUP-1",
            "category": "Other",
            "quantity": "1",
            "price": "10",
            "supplier": ""
        },
        follow_redirects=True
    )

    assert b"SKU already exists" in response.data
