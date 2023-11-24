from PySide6.QtCore import Signal, Slot
from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QTextEdit, QLineEdit, QHBoxLayout


class QChat(QWidget):
    event_triggered = Signal(str)

    def __init__(self) -> None:
        super().__init__()

        self.chat_area = QTextEdit(self)
        self.chat_area.setReadOnly(True)
        self.input_box = QLineEdit(self)

        # create button
        button = QPushButton("Send")
        button.clicked.connect(self.on_button_click)

        # Créer un layout vertical
        layout = QVBoxLayout()
        layout_msg_btn = QHBoxLayout()
        layout.addWidget(self.chat_area)

        layout_msg_btn.addWidget(self.input_box)
        layout_msg_btn.addWidget(button)

        layout.addLayout(layout_msg_btn)

        self.setFixedSize(400, 150)

        self.setLayout(layout)

    def add_message(self, message:str):
        self.chat_area.append(message)
        self.chat_area.moveCursor(QTextCursor.End)  # defiler vers le bas

    def on_button_click(self) -> None:
        message = self.input_box.text()
        self.input_box.clear()
        self.event_triggered.emit(message)
