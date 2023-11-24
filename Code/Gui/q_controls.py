from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QTextEdit, QLineEdit, QHBoxLayout

from GameEngine.const_action import ACTION_PLACE_ENTITY
from Gui.q_chat import QChat


class QControls(QWidget):
    btn_poser = Signal(int)

    def __init__(self) -> None:
        super().__init__()

        # create label
        label = QLabel("Hello, World!")
        self.q_chat = QChat()

        btn_poser = QPushButton("Poser")
        btn_poser.clicked.connect(self.btn_poser_clicked)

        # Créer un layout vertical
        layout = QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(btn_poser)
        layout.addWidget(self.q_chat)

        # Définir le layout pour le widget principal
        self.setLayout(layout)

    @Slot()
    def btn_poser_clicked(self):
        self.btn_poser.emit(ACTION_PLACE_ENTITY)
