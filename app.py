
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

FOOD_SEARCH = "https://world.openfoodfacts.org/cgi/search.pl"

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





@app.route('/')
def home():
    return jsonify({"message": "API is running"})


@app.route("/products", methods=["GET"])
def get_memory_product():
    return jsonify(products), 200



@app.route('/products/api/view', methods=["GET"])
def get_api_product():

    try:
        response = requests.get(
            "https://world.openfoodfacts.org/cgi/search.pl",
            params={
                "search_terms": "oreo",
                "search_simple": 1,
                "action": "process",
                "json": 1,
                "page_size": 10
            },
            headers={
                "User-Agent": "InventoryManagementApp/1.0"
            },
            timeout=10
        )

        if response.status_code != 200:
            return jsonify({
                "message": "OpenFoodFacts unavailable"
            }), 503


        data = response.json()

        result = []

        for item in data.get("products", []):

            result.append({
                "product_name": item.get("product_name", "Unknown"),
                "brands": item.get("brands", "Unknown"),
                "ingredients_text": item.get(
                    "ingredients_text",
                    "Unknown"
                )
            })


        return jsonify(result), 200


    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500



@app.route('/products/<int:id>', methods=["GET"])
def get_product(id):

    product = next((p for p in products if p["id"] == id), None)

    if not product:
        return jsonify({"message": "Product not found"}), 404

    return jsonify(product), 200

@app.route("/products/api/add/<product_name>", methods=["POST"])
def add_apiproduct(product_name):

    product = fetch_product(product_name)

    if product is None:
        return jsonify({
            "message": "OpenFoodFacts unavailable or product not found"
        }), 503


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


@app.route("/products/api/search/<product_name>", methods=["GET"])
def search_product(product_name):

    product = fetch_product(product_name)

    if product is None:
        return jsonify({
            "message": "OpenFoodFacts unavailable or product not found"
        }), 503

    return jsonify(product), 200



def fetch_product(product_name):

    try:
        response = requests.get(
            FOOD_SEARCH,
            params={
                "search_terms": product_name,
                "search_simple": 1,
                "action": "process",
                "json": 1,
                "page_size": 1
            },
            headers={
                "User-Agent": "InventoryManagementApp/1.0"
            },
            timeout=20
        )

        print("URL:", response.url)
        print("STATUS:", response.status_code)

        if response.status_code != 200:
            print(response.text[:200])
            return None

        data = response.json()

    except Exception as e:
        print("ERROR:", e)
        return None


    products_found = data.get("products", [])


    if not products_found:
        return None


    product = products_found[0]


    return {
        "product_name": product.get(
            "product_name",
            "Unknown"
        ),

        "brands": product.get(
            "brands",
            "Unknown"
        ),

        "ingredients_text": product.get(
            "ingredients_text",
            "Unknown"
        ),

        "categories": product.get(
            "categories",
            "Unknown"
        ),

        "countries": product.get(
            "countries",
            "Unknown"
        ),

        "nutriscore_grade": product.get(
            "nutriscore_grade",
            "Unknown"
        ),

        "image_url": product.get(
            "image_url",
            "Unknown"
        )
    }




if __name__ == "__main__":
    app.run(port=5555, debug=True)