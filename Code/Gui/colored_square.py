from PySide6.QtCore import QObject
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QGraphicsRectItem, QGraphicsSceneMouseEvent
from PySide6.scripts.metaobjectdump import Signal
import sys
from PySide6.QtWidgets import QGraphicsRectItem, QGraphicsSceneMouseEvent, QApplication, QGraphicsScene, QGraphicsRectItem, QGraphicsView, QVBoxLayout, QWidget, QLabel
from PySide6.QtCore import Qt, QRectF, QTimerEvent, QTimer, Slot, Signal, QObject


class ColoredSquare(QObject, QGraphicsRectItem):
    clicked = Signal(object)

    def __init__(self, x, y, size_x, size_y, color, entity_id):
        super().__init__()
        QGraphicsRectItem.__init__(self, x, y, size_x, size_y)
        self.setBrush(color)
        self.pos_x = x
        self.pos_y = y
        self.entity_id = entity_id

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        if self.brush().color() == Qt.blue:
            self.clicked.emit(self.entity_id)


