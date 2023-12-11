from PySide6.QtCore import QTimer, QRectF, QPointF, Slot
from PySide6.QtGui import Qt, QColor
from PySide6.QtWidgets import QGraphicsScene, QGraphicsSceneMouseEvent

from Entity.town_center import TownCenter
from GameEngine.gameplay import Gameplay
from Gui.colored_square import ColoredSquare
from Entity.human import Human
from Entity.tower import Tower
from Gui.const_image_name import *
from Gui.image_human import ImageHuman
from Gui.q_image_background import QImageBackground


class GameScene(QGraphicsScene):
    def __init__(self, gameplay: Gameplay, client_id: str) -> None:
        super().__init__()
        self.gameplay = gameplay
        self.client_id = client_id

        # timer to reset vue
        self.timer: QTimer = QTimer()
        self.timer.timeout.connect(self.update_vue)
        self.timer.start(200)

        self.squares = []
        self.update_vue()

        # Définir la taille de la scène sur une valeur très grande
        self.setSceneRect(QRectF(0, 0, 2000, 2000))
        self.setBackgroundBrush(QColor("green"))

        image_background = QImageBackground(0, 0, 2000, 2000, IMAGE_BACKGROUND, None)
        self.addItem(image_background)

    def update_vue(self) -> None:
        for square in self.squares:
            self.removeItem(square)  # Supprime chaque carré de la scène

        self.squares = []

        for i in self.gameplay.entity:
            if i.player_name == self.client_id:
                if isinstance(i, Human):
                    new_square = ImageHuman(i.pos_x, i.pos_y, i.size_x, i.size_y, IMAGE_HUMAN_BLUE, i.id)
                elif isinstance(i, TownCenter):
                    new_square = ImageHuman(i.pos_x, i.pos_y, i.size_x, i.size_y, IMAGE_TOWN_CENTER_BLUE, i.id)
                elif isinstance(i, Tower):
                    new_square = ImageHuman(i.pos_x, i.pos_y, i.size_x, i.size_y, IMAGE_TOWN_CENTER_BLUE, i.id)
                else:
                    new_square = ImageHuman(i.pos_x, i.pos_y, i.size_x, i.size_y, IMAGE_WALL_BLUE, i.id)
            else:
                if isinstance(i, Human):
                    new_square = ImageHuman(i.pos_x, i.pos_y, i.size_x, i.size_y, IMAGE_HUMAN_RED, i.id)
                elif isinstance(i, TownCenter):
                    new_square = ImageHuman(i.pos_x, i.pos_y, i.size_x, i.size_y, IMAGE_TOWN_CENTER_RED, i.id)
                elif isinstance(i, Tower):
                    new_square = ImageHuman(i.pos_x, i.pos_y, i.size_x, i.size_y, IMAGE_TOWN_CENTER_RED, i.id)
                else:
                    new_square = ImageHuman(i.pos_x, i.pos_y, i.size_x, i.size_y, IMAGE_WALL_RED, i.id)

            self.squares.append(new_square)
            self.addItem(new_square)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        item = self.itemAt(event.scenePos(), self.views()[0].transform())
        # if instance entity
        if isinstance(item, ColoredSquare) or isinstance(item, ImageHuman):
            self.gameplay.click_entity(item.entity_id)
        else:
            self.gameplay.click_screen(event)
