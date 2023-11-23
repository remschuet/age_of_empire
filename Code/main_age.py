import sys
from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget

from GameEngine.game_scene import GameScene
from GameEngine.game_listener import GameListener
from GameEngine.gameplay import Gameplay
from Gui.q_controls import QControls
from Serveur.client import Client

game_scene = None


def handle_event(message: str) -> None:
    global game_scene
    data = message.split(";")
    if data[0] == "entity":
        game_scene.gameplay.create_entity(int(data[1]), int(data[2]))  # Convertir les chaînes en entiers
    else:
        print(f"Received message from client: {message}")


def main():
    global game_scene
    app = QApplication(sys.argv)

    # gameplay part
    gameplay = Gameplay()

    game_scene = GameScene(gameplay)

    # server part
    client = Client()
    client.eventTriggered.connect(handle_event)

    game_view = GameListener(game_scene)
    q_controls = QControls()
    q_controls.q_chat.event_triggered.connect(client.send_message)

    client.eventTriggered.connect(q_controls.q_chat.add_message)  # FIX ME


    # Add graphical elements in Layout
    layout = QVBoxLayout()
    layout.addWidget(game_view)
    layout.addWidget(q_controls)

    # add layout in window
    window = QWidget()
    window.setLayout(layout)
    window.resize(600, 500)
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
