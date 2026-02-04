import socket  # socket operations
import json  # For JSON encoding/decoding

class Client:
    def __init__(self, host, port):
        # Initialise the client socket and connect to the server.
        # host: Server hostname or IP address
        # port: Server port number
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object
        self.s.connect((host, port))  # Connect to the server

    def display_products(self):
        self.s.sendall(b'VIEW_PRODUCTS')  # Send request to view products
        products = self.s.recv(1024).decode('utf-8')  # Receive product list from the server
        product_list = json.loads(products)  # Parse JSON response into a Python list
        print("\nAvailable Products:")
        for product in product_list:
            print(f"ID: {product['id']} | Name: {product['name']} | Price: £{product['price']} | Stock: {product['stock']}")

    def add_to_cart(self, product_id, quantity):
        self.s.sendall(f'ADD_TO_CART {product_id} {quantity}'.encode('utf-8'))  # Send add-to-cart request
        response = self.s.recv(1024).decode('utf-8')  # Receive server's response
        self.log_transaction(f"Added to cart: Product ID {product_id}, Quantity {quantity}")
        print(response)

    def view_cart(self):
        self.s.sendall(b'VIEW_CART')  # Send request to view cart
        cart_contents = self.s.recv(1024).decode('utf-8')  # Receive cart contents
        cart = json.loads(cart_contents)  # Parse JSON response into a Python list
        print("\nYour Cart:")
        for item in cart:
            print(f"ID: {item['id']} | Name: {item['name']} | Quantity: {item['quantity']} | Price: £{item['price']}")

    def checkout(self):
        self.s.sendall(b'CHECKOUT')  # Send checkout request
        response = self.s.recv(1024).decode('utf-8')  # Receive server's response
        print(f"Server response: {response}")  # Debugging output

        # Log the result of the checkout process
        self.log_transaction(f"Checkout response: {response}")

    def close(self):
        self.s.close()  # Close the socket connection

    def log_transaction(self, message):
        # Log the transaction details to the transaction.txt file
        with open('transaction.txt', 'a') as file:
            file.write(f"{message}\n")


def main(): # clients purchase process 
    try:
        client = Client('localhost', 5000)
    except Exception as e:
        print(f"Error connecting to server: {e}")
        return

    print('\nWelcome to the shopping system')
    try:
        while True:
            print("\nClient Menu:")
            print("1. View Products")
            print("2. Add to Cart")
            print("3. View Cart")
            print("4. Checkout")
            print("5. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                client.display_products()
            elif choice == '2':
                try:
                    product_id = int(input("Enter Product ID: "))
                    quantity = int(input("Enter Quantity: "))
                    if quantity <= 0:
                        print("Quantity must be a positive integer.")
                        continue
                    client.add_to_cart(product_id, quantity) # passing product_id and quantity with client.add_to_cart
                except ValueError:
                    print("Invalid input. Please enter numbers only.")
            elif choice == '3':
                client.view_cart()
            elif choice == '4':
                client.checkout()
            elif choice == '5':
                print("Thank You For Your Purchase!!")
                break
            else:
                print("Invalid choice. Please try again.")
    finally:
        client.close()

if __name__ == "__main__":
    main()
