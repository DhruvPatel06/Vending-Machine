import socket

def client_program():
    host = 'localhost'
    port = 5000

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    while True:
        message = input("Enter command (VIEW_PRODUCTS, ADD_TO_CART <id> <quantity>, VIEW_CART, CHECKOUT, or EXIT): ")
        if message == 'EXIT':
            break

        client_socket.send(message.encode())
        response = client_socket.recv(1024).decode()
        print('Server response:', response)

    client_socket.close()

if __name__ == '__main__':
    client_program()
