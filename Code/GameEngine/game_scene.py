from PySide6.QtCore import QTimer, QRectF, QPointF, Slot
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QGraphicsScene, QGraphicsSceneMouseEvent

from GameEngine.gameplay import Gameplay
from Gui.colored_square import ColoredSquare
from Entity.human import Human


class GameScene(QGraphicsScene):
    def __init__(self, gameplay: Gameplay) -> None:
        super().__init__()
        self.gameplay = gameplay

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
            new_square = ColoredSquare(i.pos_x, i.pos_y, 50, Qt.red, i.id)

            self.squares.append(new_square)
            self.addItem(new_square)  # Ajoute les nouveaux carrés à la scène

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        item = self.itemAt(event.scenePos(), self.views()[0].transform())
        # if instance entity
        if isinstance(item, ColoredSquare):
            self.gameplay.current_entity_id = item.entity_id
        else:
            scene_pos = event.scenePos()
            self.gameplay.click_screen((scene_pos.x() - self.gameplay.decalage_x,
                                       scene_pos.y() - self.gameplay.decalage_y))
            if self.gameplay.current_entity_id:
                entity_obj = next((rect for rect in self.gameplay.entity if rect.id == self.gameplay.current_entity_id), None)
                entity_obj.direction = (scene_pos.x() - self.gameplay.decalage_x, scene_pos.y() - self.gameplay.decalage_y)
