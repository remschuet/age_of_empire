import sys
from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget

from GameEngine.game_scene import GameScene
from GameEngine.game_listener import GameListener
from GameEngine.gameplay import Gameplay
from Gui.q_controls import QControls
from Gui.q_lobby import LobbyApp
from Serveur.client import Client


class Main:
    def __init__(self, app):
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
                if data[1] == "entity":
                    self.gameplay.received_create_entity(data[0], int(data[2]), int(data[3]))
                elif data[1] == "tower":
                    self.gameplay.received_create_tower(data[0], int(data[2]), int(data[3]))
                elif data[1] == "bouger":
                    self.gameplay.received_direction_entity(int(data[2]), float(data[3]), float(data[4]))
                elif data[1] == "attack":
                    self.gameplay.received_human_attack(int(data[2]), int(data[3]))
                elif data[1] == "town_center":
                    self.gameplay.received_create_town_center(data[0], int(data[2]), int(data[3]))
                elif data[1] == "end_game":
                    self.gameplay.received_end_game(data[0])
                    self.window.close()
                    self.window = LobbyApp()
                    self.window.show()
            else:
                print(f"Received message from client: {message}")
        # not in game
        else:
            if data[1] == "start":
                self.start_game(self.client_id == data[0])
            else:
                print("NO EVENT START")

    def start_game(self, is_starter: bool):
        # gameplay part
        self.gameplay = Gameplay(self.client_id)
        self.gameplay.action.connect(self.client.send_message)
        self.gameplay.emit_create_town_center(is_starter)

        self.game_scene = GameScene(self.gameplay, self.client_id)
        self.game_listener = GameListener(self.game_scene)

        q_controls = QControls()
        q_controls.q_chat.event_triggered.connect(self.client.send_message)
        q_controls.btn_clicked.connect(self.gameplay.received_action)

        self.client.eventTriggered.connect(q_controls.q_chat.add_message)

        # Add graphical elements in Layout
        layout = QVBoxLayout()
        layout.addWidget(self.game_listener)
        layout.addWidget(q_controls)

        # add layout in window
        self.window = QWidget()
        self.window.setLayout(layout)
        self.window.resize(600, 500)

        self.window.show()

    def btn_start_clicked(self):
        self.client.send_message(f"{self.client_id};start")


def main():
    app = QApplication(sys.argv)
    m = Main(app)
    m.window.btn_start.connect(m.btn_start_clicked)
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
