import socket
import threading

from Serveur.const import HOST_NAME, PORT_NUMBER


def handle_client(client_socket, address, clients):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break

            message = data.decode('utf-8')
            print(f"Received message from {address}: {message}")

            # Envoyer le message à tous les clients connectés
            for c in clients:
                # if c != client_socket:
                c.send(data)
        except Exception as e:
            print(f"Error handling client {address}: {e}")
            break

    print(f"Connection from {address} closed.")
    clients.remove(client_socket)
    client_socket.close()

def start_server():
    host = HOST_NAME
    port = PORT_NUMBER

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)

    print(f"Server listening on {host}:{port}")

    clients = []

    while True:
        client_socket, address = server.accept()
        print(f"Accepted connection from {address}")
        clients.append(client_socket)

        client_handler = threading.Thread(target=handle_client, args=(client_socket, address, clients))
        client_handler.start()


if __name__ == "__main__":
    start_server()
