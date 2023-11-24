from PySide6.QtCore import QTimer, QRectF, QPointF, Slot
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QGraphicsScene, QGraphicsSceneMouseEvent

from GameEngine.gameplay import Gameplay
from Gui.colored_square import ColoredSquare
from Entity.human import Human


class GameScene(QGraphicsScene):
    def __init__(self, gameplay: Gameplay, client_id: str) -> None:
        super().__init__()
        self.gameplay = gameplay
        self.client_id = client_id

        # timer to reset vue
        self.timer: QTimer = QTimer()
        self.timer.timeout.connect(self.update_vue)
        self.timer.start(200)

        self.squares: [ColoredSquare] = []
        self.update_vue()

        # Définir la taille de la scène sur une valeur très grande
        self.setSceneRect(QRectF(-10000, -10000, 20000, 20000))

    def update_vue(self) -> None:
        for square in self.squares:
            self.removeItem(square)  # Supprime chaque carré de la scène

        self.squares: [ColoredSquare] = []

        for i in self.gameplay.entity:
            if i.player_name == self.client_id:
                new_square = ColoredSquare(i.pos_x, i.pos_y, i.size, Qt.blue, i.id)
            else:
                new_square = ColoredSquare(i.pos_x, i.pos_y, i.size, Qt.red, i.id)

            self.squares.append(new_square)
            self.addItem(new_square)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        item = self.itemAt(event.scenePos(), self.views()[0].transform())
        # if instance entity
        if isinstance(item, ColoredSquare):
            self.gameplay.click_entity(item.entity_id)
        else:
            self.gameplay.click_screen(event)
