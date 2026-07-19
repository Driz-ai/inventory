      
import requests

API = "http://127.0.0.1:5555/products"



def view_inventory():
    r = requests.get(API)

    print("Status:", r.status_code)
    print(r.json())



def view_api_products():

    r = requests.get(f"{API}/api/view")

    print("Status:", r.status_code)

    if r.status_code == 200:
        print(r.json())
    else:
        print(r.text)



def add_product():
    name = input("Product name: ")
    brand = input("Brand: ")

    payload = {
        "product": {
            "product_name": name,
            "brands": brand
        }
    }

    r = requests.post(API, json=payload)

    print("Status:", r.status_code)
    print(r.json())



def update_status():
    product_id = input("Product ID: ")
    status = input("New status (0 or 1): ")

    r = requests.patch(
        f"{API}/{product_id}",
        json={
            "status": int(status)
        }
    )

    print(r.json())



def delete_product():
    product_id = input("Product ID: ")

    r = requests.delete(
        f"{API}/{product_id}"
    )

    print(r.json())



def search_food():
    name = input("Search food: ")

    r = requests.get(
        f"{API}/api/search/{name}"
    )

    print("Status:", r.status_code)
    print(r.json())



def add_api_product():
    name = input("Import product name: ")

    r = requests.post(
        f"{API}/api/add/{name}"
    )

    print("Status:", r.status_code)
    print(r.json())



if __name__ == "__main__":

    while True:

        print("""
========= Inventory Menu =========

1. View inventory (memory)
2. View OpenFoodFacts API
3. Add manual product
4. Update product status
5. Delete product
6. Search OpenFoodFacts
7. Add OpenFoodFacts product
8. Exit

==================================
""")

        choice = input("Choose option: ")


        if choice == "1":
            view_inventory()

        elif choice == "2":
            view_api_products()

        elif choice == "3":
            add_product()

        elif choice == "4":
            update_status()

        elif choice == "5":
            delete_product()

        elif choice == "6":
            search_food()

        elif choice == "7":
            add_api_product()

        elif choice == "8":
            break

        else:
            print("Invalid option")