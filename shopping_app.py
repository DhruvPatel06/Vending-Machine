import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import socket
import json

# Inventory data
inventory = [
    {'id': 1, 'name': 'Python Programming eBook', 'price': 10.99, 'stock': 25},
    {'id': 2, 'name': 'Photo Editing License', 'price': 29.99, 'stock': 17},
    {'id': 3, 'name': 'Study Playlist MP3', 'price': 5.99, 'stock': 17},
    {'id': 4, 'name': 'Adobe Photoshop', 'price': 19.99, 'stock': 25},
    {'id': 5, 'name': 'Mystery Gift', 'price': 20.99, 'stock': 15},
    {'id': 6, 'name': 'Amazon Gift Card', 'price': 10.99, 'stock': 20}
]

class ShoppingClient:
    def __init__(self, client_socket):
        self.client_socket = client_socket
        self.cart = {}  # Dictionary to store products added to the cart
        self.root = tk.Tk()
        self.root.title("Shopping System")
        self.display_products()  # Display the available products

    def display_products(self):
        #Displays the products available in the inventory.
        tk.Label(self.root, text="Available Products", font=("Arial", 16)).pack(pady=10)
        for product in inventory:
            frame = tk.Frame(self.root)
            frame.pack(pady=5, padx=10, fill="x")
            product_info = f"ID: {product['id']} | Name: {product['name']} | Price: £{product['price']} | Stock: {product['stock']}"
            tk.Label(frame, text=product_info, font=("Arial", 12)).pack(side="left")
            tk.Button(frame, text="Add to Cart", command=lambda p=product: self.prompt_quantity(p['id'], p['name'])).pack(side="right")
        tk.Button(self.root, text="View Cart", command=self.show_cart, bg="green", fg="white").pack(pady=10)

    def prompt_quantity(self, product_id, product_name):
        #Prompts the user to enter a quantity for the selected product.
        quantity_window = tk.Toplevel(self.root)
        quantity_window.title(f"Add {product_name} to Cart")
        tk.Label(quantity_window, text=f"Enter quantity for {product_name}:", font=("Arial", 12)).pack(pady=10)
        quantity_entry = tk.Entry(quantity_window, font=("Arial", 12))
        quantity_entry.pack(pady=5)

        def confirm_quantity():
            #Confirms the quantity entered and adds the product to the cart.
            try:
                quantity = int(quantity_entry.get())
                if quantity <= 0:
                    raise ValueError
                self.add_to_cart(product_id, product_name, quantity)
                quantity_window.destroy()
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid positive integer.")

        tk.Button(quantity_window, text="Confirm", command=confirm_quantity, bg="blue", fg="white").pack(pady=10)

    def add_to_cart(self, product_id, product_name, quantity):
        #Adds the specified quantity of the product to the cart, checking available stock.
        product = next((item for item in inventory if item['id'] == product_id), None)
        if product:
            # Check if the requested quantity is available
            if product['stock'] >= quantity:
                self.cart[product_id] = self.cart.get(product_id, 0) + quantity
                product['stock'] -= quantity  # Deduct the quantity from the stock
                messagebox.showinfo("Cart Updated", f"Added {quantity} of {product_name} to the cart.")
            else:
                messagebox.showerror("Stock Unavailable", f"Only {product['stock']} of {product_name} available.")
        else:
            messagebox.showerror("Product Not Found", f"Product ID {product_id} not found in inventory.")

    def show_cart(self):
        #Displays the contents of the cart.
        cart_window = tk.Toplevel(self.root)
        cart_window.title("Your Cart")
        tk.Label(cart_window, text="Your Cart", font=("Arial", 16)).pack(pady=10)
        total_cost = 0

        for product_id, quantity in self.cart.items():
            product = next((item for item in inventory if item['id'] == product_id), None)
            if product:
                cost = product['price'] * quantity
                total_cost += cost
                cart_item = f"Name: {product['name']} | Quantity: {quantity} | Price: £{cost:.2f}"
                tk.Label(cart_window, text=cart_item).pack()
            else:
                tk.Label(cart_window, text=f"Error retrieving details for product ID: {product_id}").pack()

        tk.Label(cart_window, text=f"Total: £{total_cost:.2f}", font=("Arial", 14)).pack(pady=10)
        tk.Button(cart_window, text="Checkout", command=lambda: self.prompt_payment(total_cost), bg="blue", fg="white").pack(side="left", padx=10)
        tk.Button(cart_window, text="Clear Cart", command=lambda: self.clear_cart(cart_window), bg="red", fg="white").pack(side="right", padx=10)

    def prompt_payment(self, total_cost):
        #Prompts the user to select a payment method and handles insufficient funds.
        payment_window = tk.Toplevel(self.root)
        payment_window.title("Select Payment Method")
        tk.Label(payment_window, text="Select Payment Method", font=("Arial", 16)).pack(pady=10)

        selected_payment = tk.StringVar(value="Mastercard")

        tk.Radiobutton(payment_window, text="Mastercard", variable=selected_payment, value="Mastercard", font=("Arial", 12)).pack(pady=5)
        tk.Radiobutton(payment_window, text="Visa", variable=selected_payment, value="Visa", font=("Arial", 12)).pack(pady=5)
        tk.Radiobutton(payment_window, text="Bitcoin Wallet", variable=selected_payment, value="Bitcoin Wallet", font=("Arial", 12)).pack(pady=5)

        def confirm_payment():
            payment_method = selected_payment.get()
            if self.check_funds(payment_method, total_cost):
                self.process_checkout()
                payment_window.destroy()
            else:
                messagebox.showerror("Insufficient Funds", f"Insufficient funds on {payment_method}. Please select another payment method.")
                payment_window.destroy()
                self.prompt_payment(total_cost)

        tk.Button(payment_window, text="Confirm", command=confirm_payment, bg="blue", fg="white").pack(pady=10)

    def check_funds(self, payment_method, total_cost):
        #Checks if the selected payment method has sufficient funds (dummy check for this example).
        if payment_method == "Bitcoin Wallet":
            return False  # Simulate insufficient funds for Bitcoin Wallet
        return True  # Assume sufficient funds for other payment methods

    def process_checkout(self):
        #Processes the checkout by sending the cart details to the server.
        messagebox.showinfo("Checkout Successful", "Your order has been placed successfully!")
        self.cart = {}  # Clear cart after successful checkout

    def clear_cart(self, cart_window):
        #Clears the cart and refreshes the cart view.
        self.cart = {}
        cart_window.destroy()
        messagebox.showinfo("Cart Cleared", "Your cart has been cleared.")

def main():
    # Dummy client socket for demonstration
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 5000))

    app = ShoppingClient(client_socket)
    app.root.mainloop()
    client_socket.close()

if __name__ == "__main__":
    main()
