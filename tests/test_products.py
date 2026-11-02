from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == ("Product Management API is running")


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_product():
    response = client.post(
        "/products",
        json={
            "name": "Laptop",
            "price": 55000,
            "description": "Dell laptop",
        },
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Laptop"


def test_get_products():
    response = client.get("/products")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_product_not_found():
    response = client.get("/products/99999")

    assert response.status_code == 404


def test_create_product_invalid_price():
    response = client.post(
        "/products",
        json={
            "name": "Laptop",
            "price": -100,
            "description": "Invalid product",
        },
    )

    assert response.status_code == 422
