
from flask import Flask , request , jsonify
import requests
app = Flask(__name__)

products = [
    {
        "id": 1,
        "status": 1,
        "product": {
            "barcode": "3017620422003",
            "product_name": "Organic Almond Milk",
            "brands": "Silk",
            "categories": "Plant-Based Milk",
            "ingredients_text": "Filtered water, organic almonds, cane sugar, sea salt, vitamins",
            "allergens": ["Almonds"],
            "nutriments": {
                "calories": 60,
                "fat": 2.5,
                "protein": 1,
                "carbohydrates": 8,
                "sugar": 7
            },
            "quantity": "1 L",
            "nutrition_grade": "B",
            "countries": "Canada"
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


@app.route("/products/api/add/<product_name>", methods=["POST"])
def add_apiproduct(product_name):
    product = fetch_product(product_name)

    if not product:
        return jsonify({"message" : "Product not found in openfoodfacts"})
    

    new_id = max(p["id"] for p in products) + 1 if products else 1


    new_item = {
        "id": new_id,
        "status": 1,
        "product": product
    }
    products.append(new_item)

    return jsonify(new_item),201







@app.route('/products/<int:id>', methods=["GET"])
def get_product(id):
    product = next((p for p in products if p["id"] == id), None)

    if not product:
        return jsonify({"message" : "Product not found"}),404
    
    return jsonify(product),200

@app.route('/products', methods=["POST"])
def create():
    data = request.get_json()

    if not data:
        return jsonify({"message" : "Data not found"}), 400
    
    new_id = max(product["id"] for product in products) + 1 if products else 1


    new_product = {
        "id" : new_id,
        "status" : 1,
        "product" : data["product"]
    }
    products.append(new_product)
    return jsonify(new_product), 201

@app.route('/products/<int:id>', methods=["PATCH"])
def update(id):

    data = request.get_json()

    product = next((p for p in products if p["id"] == id), None)


    if not product:
        return jsonify({"message" : "product not found"}), 400
    
  
    
    if "status" in data:
        product["status"] = data["status"]

    return jsonify(product)

@app.route('/products/<int:id>', methods=["DELETE"])
def delete(id):
    product = next((p for p in products if p["id"] == id), None)

    if not product:
        return jsonify({"message" : "product not found"}), 400
    
    products.remove(product)

    return jsonify({"message" : "Product deleted"}), 200


@app.route("/products/API/search/<product_name>", methods=["GET"])
def search_product(product_name):

    product = fetch_product(product_name)

    if not product:
        return jsonify({"message": "Product not found in OpenFoodFacts"}), 404

    return jsonify(product), 200

def fetch_product(product_name):
    response = requests.get(
        FOOD_SEARCH,
        params={
            "search_terms": product_name,
            "json": 1
        }
    )

    if response.status_code != 200:
        return None

    data = response.json()

    products = data.get("products", [])

    if not products:
        return None

    return products[0]

    
     
if __name__ == "__main__":
    app.run(port=5555 , debug=True)