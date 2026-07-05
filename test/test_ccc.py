import builtins
import requests
import ccc


# FAKE RESPONSE CLASS
class FakeResponse:
    def __init__(self, data):
        self._data = data

    def json(self):
        return self._data



# TEST SHOW ALL
def test_show_all(monkeypatch):

    monkeypatch.setattr(
        requests,
        "get",
        lambda url: FakeResponse([{"id": 1, "product": "Milk"}])
    )

    ccc.show_all()



# TEST ADD PRODUCT
def test_add_product(monkeypatch):

    inputs = iter(["Milk", "Nestle"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))

    monkeypatch.setattr(
        requests,
        "post",
        lambda url, json: FakeResponse({"id": 1, "message": "created"})
    )

    ccc.add_product()



# TEST UPDATE STATUS
def test_update_status(monkeypatch):

    inputs = iter(["1", "1"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))

    monkeypatch.setattr(
        requests,
        "patch",
        lambda url, json: FakeResponse({"id": 1, "status": 1})
    )

    ccc.update_status()



# TEST DELETE PRODUCT
def test_delete_product(monkeypatch):

    inputs = iter(["1"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))

    monkeypatch.setattr(
        requests,
        "delete",
        lambda url: FakeResponse({"message": "deleted"})
    )

    ccc.delete_product()



# TEST SEARCH PRODUCT
def test_search_product(monkeypatch):

    inputs = iter(["milk"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))

    monkeypatch.setattr(
        requests,
        "get",
        lambda url: FakeResponse({"product_name": "Milk"})
    )

    ccc.search_product()



# TEST ADD API PRODUCT
def test_add_apiproduct(monkeypatch):

    inputs = iter(["milk"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))

    monkeypatch.setattr(
        requests,
        "post",
        lambda url: FakeResponse({"id": 1, "source": "openfoodfacts"})
    )

    ccc.add_apiproduct()