from PySide6.QtCore import Signal
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton


class LobbyApp(QWidget):
    btn_start = Signal()

    def __init__(self):
        super().__init__()

        # Créer le layout vertical
        self.layout = QVBoxLayout()

        # Créer le bouton "Jouer"
        self.play_button = QPushButton("Jouer")
        self.play_button.clicked.connect(self.on_play_button_clicked)
        self.resize(600, 500)

        # Ajouter le bouton au layout
        self.layout.addWidget(self.play_button)

        # Ajouter le layout à la fenêtre
        self.setLayout(self.layout)

    def on_play_button_clicked(self):
        self.btn_start.emit()


if __name__ == "__main__":
    app = QApplication([])

    window = LobbyApp()
    window.show()
    # window.close()
    app.exec()
