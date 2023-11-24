import sys
from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget

from GameEngine.game_scene import GameScene
from GameEngine.game_listener import GameListener
from GameEngine.gameplay import Gameplay
from Gui.q_controls import QControls
from Serveur.client import Client

game_scene: GameScene = None
gameplay: Gameplay = None


def handle_event(message: str) -> None:
    global game_scene, gameplay
    data = message.split(";")
    if data[1]:
        if data[1] == "entity":
            gameplay.received_create_entity(data[0], int(data[2]), int(data[3]))
        elif data[1] == "bouger":
            gameplay.received_direction_entity(int(data[2]), float(data[3]), float(data[4]))
        elif data[1] == "attack":
            gameplay.received_human_attack(int(data[2]), int(data[3]))
    else:
        print(f"Received message from client: {message}")


def main():
    global game_scene, gameplay
    app = QApplication(sys.argv)

    # server part
    client = Client()
    client.eventTriggered.connect(handle_event)
    client_id = client.get_client_id()

    # gameplay part
    gameplay = Gameplay(client_id)
    gameplay.action.connect(client.send_message)

    game_scene = GameScene(gameplay, client_id)

    game_listener = GameListener(game_scene)
    q_controls = QControls()
    q_controls.q_chat.event_triggered.connect(client.send_message)
    q_controls.btn_poser.connect(gameplay.received_action)

    client.eventTriggered.connect(q_controls.q_chat.add_message)


    # Add graphical elements in Layout
    layout = QVBoxLayout()
    layout.addWidget(game_listener)
    layout.addWidget(q_controls)

    # add layout in window
    window = QWidget()
    window.setLayout(layout)
    window.resize(600, 500)
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
