from PySide6.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsEllipseItem, QApplication, QGraphicsRectItem
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QKeyEvent
from Gui.colored_square import ColoredSquare


class CustomGraphicsView(QGraphicsView):
    def __init__(self, scene2):
        super().__init__(scene2)
        new_square = ColoredSquare(-100, 0, 100, Qt.red, None)
        scene2.addItem(new_square)  # Ajoute les nouveaux carrés à la scène

        ellipse = QGraphicsEllipseItem(0, 0, 50, 50)
        ellipse.setBrush(Qt.red)
        scene2.addItem(ellipse)

    def keyPressEvent(self, event: QKeyEvent):
        # Si la touche vers le haut est pressée, déplace la scène vers le bas
        if event.key() == Qt.Key_Up:
            self.scene().setSceneRect(self.sceneRect().translated(0, 10))
            self.setSceneRect(QRectF(self.sceneRect().translated(0, 10)))

        # Passe l'événement à la classe parente
        super().keyPressEvent(event)


if __name__ == "__main__":
    app = QApplication([])

    # Création de la scène
    scene = QGraphicsScene()
    view = CustomGraphicsView(scene)
    view.setFixedSize(400, 400)
    view.show()

    app.exec()
