import sys
from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget

from GameEngine.game_scene import GameScene
from GameEngine.game_listener import GameListener
from GameEngine.gameplay import Gameplay
from Gui.q_controls import QControls
from Gui.q_information import QInformation
from Gui.q_lobby import LobbyApp
from Serveur.client import Client
from GameEngine.const_action import *


class Main:
    def __init__(self, app):
        self.q_information = None
        self.game_scene: GameScene = None
        self.gameplay: Gameplay = None
        self.app: QApplication = app

        # server part
        self.client = Client()
        self.client.eventTriggered.connect(self.handle_event)
        self.client_id = self.client.get_client_id()

        self.game_listener = None
        self.window = LobbyApp()
        self.window.show()

    def handle_event(self, message: str) -> None:
        # currently in game
        data = message.split(";")
        if self.gameplay:
            if data[1]:
                if int(data[1]) == ACTION_END_GAME:
                    self.gameplay.received_end_game(data[0])
                    self.window.close()
                    self.window = LobbyApp()
                    self.window.show()
                else:
                    self.gameplay.received_from_server(message)
        else:
            if data[1] == f"{ACTION_START_GAME}":
                self.start_game(self.client_id == data[0])
            else:
                print("NO EVENT START")

    def start_game(self, is_starter: bool):
        # gameplay part
        self.gameplay = Gameplay(self.client_id)
        self.gameplay.action.connect(self.client.send_message)
        self.gameplay.emit_create_town_center(is_starter)
        self.q_information = QInformation()

        self.game_scene = GameScene(self.gameplay, self.client_id)
        self.game_listener = GameListener(self.game_scene)

        q_controls = QControls()
        q_controls.q_chat.event_triggered.connect(self.client.send_message)
        q_controls.btn_clicked.connect(self.gameplay.received_action)

        self.client.eventTriggered.connect(q_controls.q_chat.add_message)

        # Add graphical elements in Layout
        layout = QVBoxLayout()
        layout.addWidget(self.q_information)
        layout.addWidget(self.game_listener)
        layout.addWidget(q_controls)

        # add layout in window
        self.window = QWidget()
        self.window.setLayout(layout)
        self.window.resize(600, 500)

        self.window.show()

    def btn_start_clicked(self):
        self.client.send_message(f"{self.client_id};{ACTION_START_GAME}")


def main():
    app = QApplication(sys.argv)
    m = Main(app)
    m.window.btn_start.connect(m.btn_start_clicked)
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
