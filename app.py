
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)


products = [
    {
        "id": 1,
        "status": 1,
        "product": {
            "product_name": "Organic Almond Milk"
        }
    },
    {
        "id": 2,
        "status": 0,
        "product": {
            "product_name": "Oreo Cookies"
        }
    }
]


FOOD_SEARCH = "https://world.openfoodfacts.org/cgi/search.pl"


@app.route('/')
def home():
    return jsonify({"message": "API is running"})



@app.route('/products', methods=["GET"])
def get_all_products():
    return jsonify(products), 200




@app.route('/products/<int:id>', methods=["GET"])
def get_product(id):

    product = next((p for p in products if p["id"] == id), None)

    if not product:
        return jsonify({"message": "Product not found"}), 404

    return jsonify(product), 200




@app.route("/products/api/add/<product_name>", methods=["POST"])
def add_apiproduct(product_name):

    product = fetch_product(product_name)

    if not product:
        return jsonify({
            "message": "Product not found in OpenFoodFacts"
        }), 404


    new_id = max(p["id"] for p in products) + 1 if products else 1


    new_item = {
        "id": new_id,
        "status": 1,
        "product": product
    }


    products.append(new_item)


    return jsonify(new_item), 201





@app.route('/products', methods=["POST"])
def create():

    data = request.get_json()

    if not data:
        return jsonify({"message": "Data not found"}), 400


    new_id = max(p["id"] for p in products) + 1 if products else 1


    new_product = {
        "id": new_id,
        "status": 1,
        "product": {
            "product_name": data["product"]["product_name"]
        }
    }


    products.append(new_product)


    return jsonify(new_product), 201





@app.route('/products/<int:id>', methods=["PATCH"])
def update(id):

    data = request.get_json()


    product = next((p for p in products if p["id"] == id), None)


    if not product:
        return jsonify({"message": "Product not found"}), 404



    if "status" in data:
        product["status"] = data["status"]


    return jsonify(product), 200





@app.route('/products/<int:id>', methods=["DELETE"])
def delete(id):

    product = next((p for p in products if p["id"] == id), None)


    if not product:
        return jsonify({"message": "Product not found"}), 404


    products.remove(product)


    return jsonify({"message": "Product deleted"}), 200



@app.route("/products/API/search/<product_name>", methods=["GET"])
def search_product(product_name):

    product = fetch_product(product_name)


    if not product:
        return jsonify({
            "message": "Product not found in OpenFoodFacts"
        }), 404


    return jsonify(product), 200



def fetch_product(product_name):

    response = requests.get(
        FOOD_SEARCH,
        params={
            "search_terms": product_name,
            "json": 1,
            "page_size": 1
        }
    )

    if response.status_code != 200:
        return None

    data = response.json()

    result = data.get("products", [])

    if not result:
        return None

    product = result[0]

    return {
        "product_name": product.get("product_name", "Unknown"),
        "brands": product.get("brands", "Unknown")
    }


if __name__ == "__main__":
    app.run(port=5555, debug=True)