from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout

from common.const_action import *


class QControlVillager(QWidget):
    btn_clicked = Signal(int)

    def __init__(self) -> None:
        super().__init__()

        label = QLabel("Villager!")

        btn_place_tower = QPushButton("Tower")
        btn_place_tower.clicked.connect(self.emit_place_tower)
        btn_place_wall = QPushButton("Wall")
        btn_place_wall.clicked.connect(self.emit_place_wall)

        # Créer un layout vertical
        layout = QHBoxLayout()
        layout.addWidget(label)

        layout.addWidget(btn_place_tower)
        layout.addWidget(btn_place_wall)

        # Définir le layout pour le widget principal
        self.setLayout(layout)

    @Slot()
    def emit_place_tower(self):
        self.btn_clicked.emit(ACTION_PLACE_TOWER)

    @Slot()
    def emit_place_wall(self):
        self.btn_clicked.emit(ACTION_PLACE_WALL)
