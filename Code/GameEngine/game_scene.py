from PySide6.QtCore import QTimer, QRectF, QPointF, Slot, Signal
from PySide6.QtGui import Qt, QColor
from PySide6.QtWidgets import QGraphicsScene, QGraphicsSceneMouseEvent

from Entity.town_center import TownCenter
from Entity.villager import Villager
from Entity.wall import Wall
from GameEngine.gameplay import Gameplay
from Gui.colored_square import ColoredSquare
from Entity.Soldier import Soldier
from Entity.tower import Tower
from Gui.const_image_name import *
from Gui.q_image_entity import QImageEntity
from Gui.q_image_background import QImageBackground
from Gui.q_information import QInformation
from Gui.q_layout_town_center import QLayoutTownCenter
from common.const_resource_entity import *


class GameScene(QGraphicsScene):
    change_control = Signal(int)

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
                if isinstance(i, Soldier):
                    new_square = QImageEntity(i.pos_x, i.pos_y, i.size_x, i.size_y, IMAGE_HUMAN_BLUE, i.id, CONST_SOLDIER)
                elif isinstance(i, Villager):
                    new_square = QImageEntity(i.pos_x, i.pos_y, i.size_x, i.size_y, IMAGE_VILLAGER_BLUE, i.id, CONST_VILLAGER)
                elif isinstance(i, TownCenter):
                    new_square = QLayoutTownCenter(i.pos_x, i.pos_y, i.size_x, i.size_y, IMAGE_TOWN_CENTER_BLUE, i.id)
                elif isinstance(i, Tower):
                    new_square = QImageEntity(i.pos_x, i.pos_y, i.size_x, i.size_y, IMAGE_TOWER_BLUE, i.id, CONST_TOWER)
                elif isinstance(i, Wall):
                    new_square = QImageEntity(i.pos_x, i.pos_y, i.size_x, i.size_y, IMAGE_WALL_BLUE, i.id, CONST_WALL)
                else:
                    new_square = QImageEntity(i.pos_x, i.pos_y, i.size_x, i.size_y, IMAGE_WALL_BLUE, i.id, CONST_NONE)
            else:
                if isinstance(i, Soldier):
                    new_square = QImageEntity(i.pos_x, i.pos_y, i.size_x, i.size_y, IMAGE_HUMAN_RED, i.id, CONST_SOLDIER)
                elif isinstance(i, Villager):
                    new_square = QImageEntity(i.pos_x, i.pos_y, i.size_x, i.size_y, IMAGE_VILLAGER_RED, i.id, CONST_VILLAGER)
                elif isinstance(i, TownCenter):
                    new_square = QLayoutTownCenter(i.pos_x, i.pos_y, i.size_x, i.size_y, IMAGE_TOWN_CENTER_RED, i.id)
                elif isinstance(i, Tower):
                    new_square = QImageEntity(i.pos_x, i.pos_y, i.size_x, i.size_y, IMAGE_TOWER_RED, i.id, CONST_TOWER)
                elif isinstance(i, Wall):
                    new_square = QImageEntity(i.pos_x, i.pos_y, i.size_x, i.size_y, IMAGE_WALL_RED, i.id, CONST_WALL)
                else:
                    new_square = QImageEntity(i.pos_x, i.pos_y, i.size_x, i.size_y, IMAGE_WALL_RED, i.id, CONST_NONE)

            self.squares.append(new_square)
            self.addItem(new_square)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        item = self.itemAt(event.scenePos(), self.views()[0].transform())
        # if instance entity
        if isinstance(item, ColoredSquare):
            self.gameplay.click_entity(item.entity_id)
        elif isinstance(item, QImageEntity):
            self.gameplay.click_entity(item.entity_id)
            self.change_control.emit(item.type_entity)
        elif isinstance(item, QLayoutTownCenter):
            self.change_control.emit(CONST_TOWN_CENTER)
        elif isinstance(item, Villager):
            self.change_control.emit(CONST_VILLAGER)
        else:
            self.gameplay.click_screen(event)
            self.change_control.emit(None)
