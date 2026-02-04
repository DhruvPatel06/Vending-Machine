import socket
import json
import threading

# Product class to represent inventory items
class Product:
    def __init__(self, product_id, name, price, stock):
        # Initialise a product with ID, name, price, and stock.
        self.id = product_id
        self.name = name
        self.price = price
        self.stock = stock

    def to_dict(self):
        # Convert the product instance to a dictionary for JSON serialization.
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'stock': self.stock
        }

    def update_stock(self, quantity):
        # Update stock by reducing the given quantity.
        # Returns True if the stock is sufficient, otherwise False.
        if self.stock >= quantity:
            self.stock -= quantity
            return True
        return False

# Inventory class to manage all products
class Inventory:
    def __init__(self):
        # Initialise the inventory and populate it with default products.
        self.products = {}  # Dictionary to store products by ID
        self._initialise_products()

    def _initialise_products(self):
        # Populates inventory with predefined products.
        product_data = [
            (1, "Python Programming eBook", 10.99, 25),
            (2, "Photo Editing License", 29.99, 17),
            (3, "Study Playlist MP3", 5.99, 17),
            (4, "Adobe Photoshop", 19.99, 25),
            (5, "Mystery Gift", 20.99, 10),
            (6, "Amazon Gift Card", 10.99, 20),
        ]
        for data in product_data:
            product = Product(*data)
            self.products[product.id] = product

    def get_product_list(self):
        # Return a list of all products as dictionaries.
        return [product.to_dict() for product in self.products.values()]

    def process_checkout(self, cart):
        # Process the checkout for a client's cart.
        # Updates stock if sufficient inventory is available.
        # Returns a tuple
        updated_products = []  # To track products updated during checkout
        try:
            for item in cart:
                product_id = item['id']
                quantity = item['quantity']
                product = self.products.get(product_id)

                if not product:
                    return False, f"Product ID {product_id} not found."
                if not product.update_stock(quantity):
                    # Rollback for previously updated products
                    for updated in updated_products:
                        updated['product'].update_stock(-updated['quantity'])
                    return False, f"Insufficient stock for {product.name}."
                updated_products.append({'product': product, 'quantity': quantity})

            return True, "successful"
        except Exception as e:
            # Rollback in case of any unexpected errors
            for updated in updated_products:
                updated['product'].update_stock(-updated['quantity'])
            return False, f"Checkout failed due to an error: {str(e)}"
'''
def get_product_details(self, product_id):
    try:
        # Request product details
        request_data = {'action': 'get_product_details', 'id': product_id}
        self.client_socket.sendall(json.dumps(request_data).encode('utf-8'))
        response = self.client_socket.recv(1024).decode('utf-8')

        print(f"Request sent: {request_data}")  # Debugging output
        print(f"Response received: {response}")  # Debugging output

        # Validate the response
        if not response:
            print(f"No response from server for product ID: {product_id}")
            return None  # No response from server
        product = json.loads(response)

        # Check required fields
        if not all(key in product for key in ('id', 'name', 'price', 'stock')):
            raise ValueError(f"Invalid product details: {product}")
        return response
    except (json.JSONDecodeError, ValueError, KeyError) as e:
        print(f"Error parsing product details for ID {product_id}: {e}")
        return None
'''
def add_to_cart(product_id, quantity, inventory, cart):
    # Adds a product to the cart and adjusts inventory stock.
    for product in inventory:
        if product['id'] == product_id:
            if product['stock'] >= quantity:
                product['stock'] -= quantity
                if product_id in cart:
                    cart[product_id]['quantity'] += quantity
                else:
                    cart[product_id] = {
                        'name': product['name'],
                        'price': product['price'],
                        'quantity': quantity
                    }
                print(f"Added {quantity} x {product['name']} to the cart.")
                print("Current cart:", cart)  # Log cart state
            else:
                print(f"Not enough stock available for {product['name']}.")
            return
    print("Invalid Product ID.")
    
def add_to_cart(product_id, quantity, inventory, cart):
    # Adds a product to the cart and adjusts inventory stock.
    for product in inventory:
        if product['id'] == product_id:
            if product['stock'] >= quantity:
                product['stock'] -= quantity
                if product_id in cart:
                    cart[product_id]['quantity'] += quantity
                else:
                    cart[product_id] = {
                        'name': product['name'],
                        'price': product['price'],
                        'quantity': quantity
                    }
                print(f"Added {quantity} x {product['name']} to the cart.")
                print("Current cart:", cart)  # Log cart state
            else:
                print(f"Not enough stock available for {product['name']}.")
            return
    print("Invalid Product ID.")

def view_cart(cart):
    # Displays the contents of the cart and calculates the total price.
    if not cart:
        print("\nYour cart is empty.")
        return
    
    print("\nCart Contents:")
    print(f"{'Product':<30} {'Quantity':<10} {'Price':<10} {'Total':<10}")
    print("-" * 60)
    total_cost = 0
    for item in cart.values():
        total = item['quantity'] * item['price']
        total_cost += total
        print(f"{item['name']:<30} {item['quantity']:<10} £{item['price']:<10.2f} £{total:<10.2f}")
    print("-" * 60)
    print(f"Total Cost: £{total_cost:.2f}")
    print("Current cart for debugging:", cart)  # Log cart state

def view_cart(cart):
    # Displays the contents of the cart and calculates the total price.
    if not cart:
        print("\nYour cart is empty.")
        return
    
    print("\nCart Contents:")
    print(f"{'Product':<30} {'Quantity':<10} {'Price':<10} {'Total':<10}")
    print("-" * 60)
    total_cost = 0
    for item in cart.values():
        total = item['quantity'] * item['price']
        total_cost += total
        print(f"{item['name']:<30} {item['quantity']:<10} £{item['price']:<10.2f} £{total:<10.2f}")
    print("-" * 60)
    print(f"Total Cost: £{total_cost:.2f}")
    print("Current cart for debugging:", cart)  # Log cart state

    
def handle_client(client_socket, inventory):
    cart = []  # Cart specific to the client
    try:
        while True:
            request = client_socket.recv(1024).decode('utf-8')
            if not request:
                break  # Exit if the client disconnects

            print(f"Received request: {request}")  # Debugging output

            if request == 'VIEW_PRODUCTS':
                product_list = inventory.get_product_list()
                response = json.dumps(product_list)
                client_socket.send(response.encode('utf-8'))

            elif request.startswith('ADD_TO_CART'):
                try:
                    _, product_id, quantity = request.split()
                    product_id = int(product_id)
                    quantity = int(quantity)
                    product = inventory.products.get(product_id)

                    if product:
                        cart_item = next((item for item in cart if item['id'] == product_id), None)
                        if cart_item:
                            cart_item['quantity'] += quantity
                        else:
                            cart.append({
                                'id': product.id,
                                'name': product.name,
                                'quantity': quantity,
                                'price': product.price
                            })
                        response = f"Added {quantity} of {product.name} to cart."
                    else:
                        response = "Product not found."
                except ValueError:
                    response = "Invalid request format for ADD_TO_CART."
                client_socket.send(response.encode('utf-8'))

            elif request == 'VIEW_CART':
                response = json.dumps(cart)
                client_socket.send(response.encode('utf-8'))

            elif request.startswith('GET_PRODUCT_DETAILS'):
                try:
                    _, product_id = request.split()
                    product_id = int(product_id)
                    product = inventory.products.get(product_id)
                    if product:
                        response = json.dumps(product.to_dict())
                    else:
                        response = json.dumps({"error": f"Product ID {product_id} not found"})
                except ValueError:
                    response = json.dumps({"error": "Invalid request format for GET_PRODUCT_DETAILS"})
                client_socket.send(response.encode('utf-8'))
                print(f"Sent response: {response}")  # Debugging output

            elif request == 'CHECKOUT':
                success, message = inventory.process_checkout(cart)
                if success:
                    cart.clear()
                response = json.dumps({'success': success, 'message': message})
                client_socket.send(response.encode('utf-8'))

            else:
                response = "Invalid command"
                client_socket.send(response.encode('utf-8'))

    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()

# Main server function remains unchanged


def server_program():
    # Main server function to accept client connections and handle requests.
    inventory = Inventory()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind(('localhost', 5000))
        server_socket.listen(5)
        print("Server is running and waiting for the connection...")

        while True:
            client_socket, _ = server_socket.accept()
            print("Client connected.")
            client_thread = threading.Thread(target=handle_client, args=(client_socket, inventory))
            client_thread.start()
    except Exception as e:
        print(f"Server error: {e}")
    finally:
        server_socket.close()

if __name__ == "__main__":
    server_program()
# constructor __main__ method 


















