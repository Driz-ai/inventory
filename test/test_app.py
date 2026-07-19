import pytest
from app import app
import app as app_module


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client



def test_home(client):

    response = client.get("/")

    assert response.status_code == 200
    assert response.json["message"] == "API is running"



def test_view_memory_products(client):

    response = client.get("/products")

    assert response.status_code == 200
    assert isinstance(response.json, list)



def test_view_openfoodfacts(client, monkeypatch):

    class FakeResponse:

        status_code = 200

        def json(self):
            return {
                "products":[
                    {
                        "product_name":"Oreo",
                        "brands":"Oreo",
                        "ingredients_text":"Sugar"
                    }
                ]
            }


    monkeypatch.setattr(
        app_module.requests,
        "get",
        lambda *args, **kwargs: FakeResponse()
    )


    response = client.get("/products/api/view")


    assert response.status_code == 200
    assert response.json[0]["product_name"] == "Oreo"



def test_get_product(client):

    response = client.get("/products/1")

    assert response.status_code == 200
    assert "product" in response.json



def test_get_product_not_found(client):

    response = client.get("/products/999")


    assert response.status_code == 404
    assert response.json["message"] == "Product not found"



def test_add_manual_product(client):

    payload = {

        "product":{
            "product_name":"Chair",
            "brands":"IKEA"
        }

    }


    response = client.post(
        "/products",
        json=payload
    )


    assert response.status_code == 201
    assert response.json["product"]["product_name"] == "Chair"



def test_update_status(client):

    response = client.patch(
        "/products/1",
        json={
            "status":0
        }
    )


    assert response.status_code == 200
    assert response.json["status"] == 0



def test_delete_product(client):

    response = client.delete(
        "/products/1"
    )


    assert response.status_code == 200
    assert response.json["message"] == "Product deleted"




def test_search_openfoodfacts(client, monkeypatch):

    class FakeResponse:

        status_code = 200
        url = "fake-url"

        def json(self):
            return {
                "products": [
                    {
                        "product_name": "Milk",
                        "brands": "Nestle",
                        "ingredients_text": "Milk"
                    }
                ]
            }

        text = "OK"


    monkeypatch.setattr(
        app_module.requests,
        "get",
        lambda *args, **kwargs: FakeResponse()
    )


    response = client.get(
        "/products/api/search/milk"
    )


    assert response.status_code == 200
    assert response.json["product_name"] == "Milk"
    assert response.json["brands"] == "Nestle"



def test_add_api_product(client, monkeypatch):


    class FakeResponse:

        status_code = 200
        url = "fake-url"

        def json(self):
            return {
                "products": [
                    {
                        "product_name": "Oreo",
                        "brands": "Oreo",
                        "ingredients_text": "Sugar"
                    }
                ]
            }

        text = "OK"



    monkeypatch.setattr(
        app_module.requests,
        "get",
        lambda *args, **kwargs: FakeResponse()
    )


    response = client.post(
        "/products/api/add/oreo"
    )


    assert response.status_code == 201

    assert response.json["product"]["product_name"] == "Oreo"
    assert response.json["product"]["brands"] == "Oreo"



