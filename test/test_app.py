import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client



def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json["message"] == "API is running"



def test_get_all_products(client):
    response = client.get("/products")
    assert response.status_code == 200



def test_get_product_valid(client):
    response = client.get("/products/1")
    assert response.status_code == 200
    assert "product" in response.json


def test_get_product_invalid(client):
    response = client.get("/products/999")
    assert response.status_code == 404
    assert response.json["message"] == "Product not found"



def test_create_product(client):
    payload = {
        "product": {
            "product_name": "Test Product",
            "brands": "Test Brand"
        }
    }

    response = client.post("/products", json=payload)
    assert response.status_code == 201
    assert response.json["product"]["product_name"] == "Test Product"



def test_update_product(client):
    response = client.patch("/products/1", json={"status": 2})
    assert response.status_code == 200
    assert response.json["status"] == 2



def test_delete_product(client):
    # first create a product to delete
    create = client.post("/products", json={
        "product": {
            "product_name": "To Delete",
            "brands": "Brand"
        }
    })

    new_id = create.json["id"]

    response = client.delete(f"/products/{new_id}")
    assert response.status_code == 200
    assert response.json["message"] == "Product deleted"