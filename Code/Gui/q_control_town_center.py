from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout

from common.const_action import *
from Gui.q_chat import QChat


class QControlTownCenter(QWidget):
    btn_clicked = Signal(int)

    def __init__(self) -> None:
        super().__init__()

        label = QLabel("Town Center!")

        btn_place_villager = QPushButton("Villager")
        btn_place_villager.clicked.connect(self.emit_place_villager)

        # Créer un layout vertical
        layout = QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(btn_place_villager)

        # Définir le layout pour le widget principal
        self.setLayout(layout)

    @Slot()
    def emit_place_villager(self):
        self.btn_clicked.emit(ACTION_PLACE_VILLAGER)
