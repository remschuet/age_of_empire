from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QTextEdit, QLineEdit, QHBoxLayout

from Gui.q_chat import QChat


class QControls(QWidget):

    def __init__(self) -> None:
        super().__init__()

        # create label
        label = QLabel("Hello, World!")
        self.q_chat = QChat()

        # Créer un layout vertical
        layout = QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.q_chat)

        # Définir le layout pour le widget principal
        self.setLayout(layout)
