import requests

API = "http://127.0.0.1:5555/products"



def show_all():
    r = requests.get(API)
    print(r.json())



def add_product():
    name = input("Product name: ")
    brand = input("Brand: ")

    payload = {
        "product": {
            "product_name": name,
            "brands": brand}
    }

    r = requests.post(API, json=payload)
    print(r.json())



def update_status():
    product_id = input("Product ID: ")
    status = input("New status (0 or 1): ")

    r = requests.patch(
        f"{API}/{product_id}",
        json={"status": int(status)}
    )

    print(r.json())



def delete_product():
    product_id = input("Product ID: ")

    r = requests.delete(f"{API}/{product_id}")
    print(r.json())



def search_product():
    name = input("Enter product name: ")

    r = requests.get(f"{API}/api/search/{name}")
    print(r.json())



def add_apiproduct():
    name = input("Enter product name: ")

    r = requests.post(f"{API}/api/add/{name}")
    print(r.json())


if __name__ == "__main__":

        while True:

            print("    Inventory Menu    ")
            print("\n1. View all products \n2. Add product\n3. Update product status\n4. Delete product\n5. Search Food\n6. Add apiproduct \n7. Exit")

            choice = input("Choose an option: ")

            if choice == "1":
                show_all()

            elif choice == "2":
                add_product()

            elif choice == "3":
                update_status()

            elif choice == "4":
                delete_product()

            elif choice == "5":
                search_product()

            elif choice == "6":
                add_apiproduct()

            elif choice == "7":
                break

            else:
                print("Invalid option. Please try again.")


       
 