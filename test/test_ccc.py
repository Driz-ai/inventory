import builtins
import requests
import ccc



class FakeResponse:

    def __init__(self, data):

        self.data = data
        self.status_code = 200


    def json(self):

        return self.data



def test_view_inventory(monkeypatch):

    monkeypatch.setattr(
        requests,
        "get",
        lambda url: FakeResponse(
            [
                {
                    "id":1,
                    "product":"Milk"
                }
            ]
        )
    )


    ccc.view_inventory()



def test_view_api_products(monkeypatch):

    monkeypatch.setattr(
        requests,
        "get",
        lambda url: FakeResponse(
            [
                {
                    "product_name":"Oreo"
                }
            ]
        )
    )


    ccc.view_api_products()




def test_add_product(monkeypatch):

    inputs = iter(
        [
            "Chair",
            "IKEA"
        ]
    )


    monkeypatch.setattr(
        builtins,
        "input",
        lambda x: next(inputs)
    )


    monkeypatch.setattr(
        requests,
        "post",
        lambda url,json: FakeResponse(
            {
                "id":3,
                "product":{
                    "product_name":"Chair"
                }
            }
        )
    )


    ccc.add_product()




def test_update_status(monkeypatch):


    inputs = iter(
        [
            "1",
            "0"
        ]
    )


    monkeypatch.setattr(
        builtins,
        "input",
        lambda x: next(inputs)
    )



    monkeypatch.setattr(
        requests,
        "patch",
        lambda url,json: FakeResponse(
            {
                "status":0
            }
        )
    )


    ccc.update_status()




def test_delete_product(monkeypatch):


    monkeypatch.setattr(
        builtins,
        "input",
        lambda x:"1"
    )


    monkeypatch.setattr(
        requests,
        "delete",
        lambda url: FakeResponse(
            {
                "message":"Product deleted"
            }
        )
    )


    ccc.delete_product()




def test_search_food(monkeypatch):


    monkeypatch.setattr(
        builtins,
        "input",
        lambda x:"milk"
    )


    monkeypatch.setattr(
        requests,
        "get",
        lambda url: FakeResponse(
            {
                "product_name":"Milk"
            }
        )
    )


    ccc.search_food()




def test_add_api_product(monkeypatch):


    monkeypatch.setattr(
        builtins,
        "input",
        lambda x:"oreo"
    )


    monkeypatch.setattr(
        requests,
        "post",
        lambda url: FakeResponse(
            {
                "id":3,
                "product_name":"Oreo"
            }
        )
    )


    ccc.add_api_product()