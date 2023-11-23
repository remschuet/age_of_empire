import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor
import socket
import threading

from Serveur.const import PORT_NUMBER, HOST_NAME


class ChatClient(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

        # Initialisation du client socket
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect_to_server()

    def init_ui(self):
        self.setWindowTitle('Chat Client')

        # Zone de texte pour afficher les messages
        self.text_area = QTextEdit(self)
        self.text_area.setReadOnly(True)

        # Zone de saisie pour écrire les messages
        self.input_box = QLineEdit(self)
        self.send_button = QPushButton('Send', self)
        self.send_button.clicked.connect(self.send_message)

        # Mise en page verticale
        layout = QVBoxLayout(self)
        layout.addWidget(self.text_area)
        layout.addWidget(self.input_box)
        layout.addWidget(self.send_button)

    def connect_to_server(self):
        host = HOST_NAME
        port = PORT_NUMBER

        try:
            self.client_socket.connect((host, port))
            self.receive_thread = threading.Thread(target=self.receive_messages)
            self.receive_thread.start()
        except Exception as e:
            print(f"Error connecting to server: {e}")
            sys.exit()

    def send_message(self):
        message = self.input_box.text()
        if message:
            self.client_socket.send(message.encode('utf-8'))
            self.input_box.clear()

    def receive_messages(self):
        while True:
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                message = data.decode('utf-8')
                self.text_area.append(f"Server: {message}")
                print(message)
                self.text_area.moveCursor(QTextCursor.End)  # Fait défiler automatiquement vers le bas
            except Exception as e:
                print(f"Error receiving message: {e}")
                break


def run_client_app():
    app = QApplication(sys.argv)
    chat_client = ChatClient()
    chat_client.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    run_client_app()
