from PySide6.QtCore import Qt, QRectF
from PySide6.QtWidgets import QGraphicsView


class GameListener(QGraphicsView):
    def __init__(self, scene) -> None:
        super().__init__(scene)
        self.move_x = 0
        self.move_y = 0

        # Activer la réception des événements clavier
        self.setFocusPolicy(Qt.StrongFocus)

        # Désactiver les barres de défilement
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def keyPressEvent(self, event) -> None:
        if event.key() == Qt.Key_Left and self.scene().sceneRect().left() > -1000:
            self.scene().setSceneRect(self.sceneRect().translated(10, 0))
        elif event.key() == Qt.Key_Right and self.scene().sceneRect().right() < 1000:
            self.scene().setSceneRect(self.sceneRect().translated(-10, 0))
        elif event.key() == Qt.Key_Up and self.scene().sceneRect().top() > -1000:
            self.scene().setSceneRect(self.sceneRect().translated(0, 10))
        elif event.key() == Qt.Key_Down and self.scene().sceneRect().bottom() < 1000:
            self.scene().setSceneRect(self.sceneRect().translated(0, -10))

        super().keyPressEvent(event)

        self.scene().update_vue()
