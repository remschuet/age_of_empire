from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout

from Gui import q_control_test
from Gui.q_control_town_center import QControlTownCenter
from Gui.q_chat import QChat
from Gui.q_control_test import QControlTest
from Gui.q_control_villager import QControlVillager
from common.const_resource_entity import *

"""
Qcontrol is a control manager offered to the user.
It makes it possible to display certain possible controls depending on the
user selections.

It sends a signal when a button is clicked (ACTION_)
It receives a change_control signal (CONST_)
"""


class QControl(QWidget):
    btn_clicked = Signal(int)

    def __init__(self) -> None:
        super().__init__()

        # create label
        self.q_chat = QChat()
        self.controls = None

        # Créer un layout vertical
        self.container_btn = QHBoxLayout()
        self.container_btn.addWidget(self.q_chat)

        self.controls = QWidget()

        # Définir le layout pour le widget principal
        self.setLayout(self.container_btn)

    def emit_signal(self, action_call: int):
        self.btn_clicked.emit(action_call)

    @Slot(int)
    def change_control(self, control_entity: int):
        self.container_btn.removeWidget(self.controls)
        self.controls.deleteLater()  # Delete the widget
        print("control_entity: ",control_entity)
        if control_entity == CONST_TOWN_CENTER:
            self.controls = QControlTownCenter()
        elif control_entity == CONST_VILLAGER:
            self.controls = QControlVillager()
        else:
            self.controls = QControlTest()

        self.container_btn.insertWidget(0, self.controls)
        self.controls.btn_clicked.connect(self.emit_signal)
