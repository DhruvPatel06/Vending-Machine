import sqlite3
import socket
import json

class InventoryDatabase:
    def __init__(self, db_path):
        self.db_path = db_path

    # Fetch all products from the database
    def get_product_list(self):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute('SELECT id, name, price, stock FROM products')
        products = cursor.fetchall()
        connection.close()
        return [{'id': p[0], 'name': p[1], 'price': p[2], 'stock': p[3]} for p in products]

    # Update the stock of a product after purchase
    def update_inventory_in_db(self, product_id, quantity):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute('UPDATE products SET stock = stock - ? WHERE id = ? AND stock >= ?', (quantity, product_id, quantity))
        updated = cursor.rowcount > 0  # Check if the update was successful
        connection.commit()
        connection.close()
        return updated

    # Save a transaction to the transactions table
    def save_transaction_in_db(self, cart):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        for item in cart:
            cursor.execute('INSERT INTO transactions (product_id, quantity, price) VALUES (?, ?, ?)',
                           (item['id'], item['quantity'], item['price']))
        connection.commit()
        connection.close()

# Function to handle client requests
def handle_client(client_socket, db):
    try:
        while True:
            request = client_socket.recv(1024).decode('utf-8')
            if not request:
                break

            request = json.loads(request)
            action = request.get('action')

            if action == 'get_product_list':
                # Retrieve products from the database
                products = db.get_product_list()
                client_socket.send(json.dumps(products).encode('utf-8'))
            elif action == 'checkout':
                # Process checkout
                cart = request.get('cart', [])
                success = True
                for item in cart:
                    if not db.update_inventory_in_db(item['id'], item['quantity']):
                        success = False
                        message = f"Insufficient stock for Product ID {item['id']}."
                        client_socket.send(json.dumps({'success': success, 'message': message}).encode('utf-8'))
                        return

                # Save the transaction if all items are available
                db.save_transaction_in_db(cart)
                client_socket.send(json.dumps({'success': True, 'message': "Checkout successful."}).encode('utf-8'))
            else:
                client_socket.send(json.dumps({'error': 'Invalid action'}).encode('utf-8'))
    finally:
        client_socket.close()

# Main server function
def server_program():
    # Initialise the database and inventory management
    db = InventoryDatabase('store.db')

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 5000))
    server_socket.listen(5)

    print("Server is running and waiting for the intial connection...")
    while True:
        client_socket, _ = server_socket.accept()
        print("Client connected.")
        handle_client(client_socket, db)

if __name__ == "__main__":
    server_program()
