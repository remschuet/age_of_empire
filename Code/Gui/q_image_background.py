from PySide6.QtCore import Qt, Signal, QObject
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QGraphicsSceneMouseEvent, QGraphicsPixmapItem
import os

# https://opengameart.org/content/lpc-medieval-fantasy-character-sprites


class QImageBackground(QObject, QGraphicsPixmapItem):
    clicked = Signal(object)

    def __init__(self, x, y, size_x, size_y, image_path, entity_id):
        super().__init__()
        QGraphicsPixmapItem.__init__(self)

        image_path = f"image/{image_path}"

        script_directory = os.path.dirname(os.path.realpath(__file__))
        image_full_path = os.path.join(script_directory, image_path)
        pixmap = QPixmap(image_full_path).scaled(size_x, size_y)

        self.setPixmap(pixmap)
        self.setPos(x, y)
        self.entity_id = entity_id
