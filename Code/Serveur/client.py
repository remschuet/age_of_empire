import random
import sys
from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QApplication
import socket
import threading

from Serveur.const import HOST_NAME, PORT_NUMBER


class Client(QObject):
    eventTriggered = Signal(str)

    def __init__(self) -> None:
        super().__init__()
        self.receive_thread = None

        # Initialisation du client socket
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect_to_server()

    def get_client_id(self):
        return f"id_{random.randint(1000, 9999)}"  # Utilisez le numéro de port comme identifiant

    def connect_to_server(self):
        host = HOST_NAME  # Adresse IP du serveur
        port = PORT_NUMBER

        try:
            self.client_socket.connect((host, port))
            self.receive_thread = threading.Thread(target=self.receive_messages)
            self.receive_thread.start()
        except Exception as e:
            print(f"Error connecting to server: {e}")
            sys.exit()

    def send_message(self, message):
        if message:
            self.client_socket.send(message.encode('utf-8'))

    def receive_messages(self):
        while True:
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                message = data.decode('utf-8')
                print(message)
                self.eventTriggered.emit(message)
            except Exception as e:
                print(f"Error receiving message: {e}")
                break


def run_client_app():
    app = QApplication(sys.argv)
    chat_client = Client()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run_client_app()
