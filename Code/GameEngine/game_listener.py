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
        if event.key() == Qt.Key_Left:
            self.scene().setSceneRect(self.sceneRect().translated(10, 0))
            self.setSceneRect(QRectF(self.sceneRect().translated(10, 0)))
            super().keyPressEvent(event)
        elif event.key() == Qt.Key_Right:
            self.scene().setSceneRect(self.sceneRect().translated(-10, 0))
            self.setSceneRect(QRectF(self.sceneRect().translated(-10, 0)))
            super().keyPressEvent(event)
        elif event.key() == Qt.Key_Up:
            self.scene().setSceneRect(self.sceneRect().translated(0, 10))
            self.setSceneRect(QRectF(self.sceneRect().translated(0, 10)))
            super().keyPressEvent(event)
        elif event.key() == Qt.Key_Down:
            self.scene().setSceneRect(self.sceneRect().translated(0, -10))
            self.setSceneRect(QRectF(self.sceneRect().translated(0, -10)))
            super().keyPressEvent(event)

        self.scene().update_vue()
