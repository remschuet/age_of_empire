from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGraphicsView


class GameView(QGraphicsView):
    def __init__(self, scene) -> None:
        super().__init__(scene)
        self.move_x = 0
        self.move_y = 0

        # Activer la réception des événements clavier
        self.setFocusPolicy(Qt.StrongFocus)

        # Désactiver les barres de défilement
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def move_element(self) -> None:
        for enti in self.scene().gameplay.entity:
            enti.pos_x += self.move_x
            enti.pos_y += self.move_y

    def keyPressEvent(self, event) -> None:
        step = 10  # Ajustez la taille du pas selon vos besoins
        if event.key() == Qt.Key_Left:
            self.move_x += step
            self.scene().gameplay.decalage_x += 10
        elif event.key() == Qt.Key_Right:
            self.move_x -= step
            self.scene().gameplay.decalage_x -= 10
        elif event.key() == Qt.Key_Up:
            self.move_y += step
            self.scene().gameplay.decalage_y += 10
        elif event.key() == Qt.Key_Down:
            self.scene().gameplay.decalage_y -= 10
            self.move_y -= step

        self.move_element()
        self.scene().update_vue()
        self.move_x = 0
        self.move_y = 0
