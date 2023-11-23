from PySide6.QtCore import QTimer, QRectF, QPointF, Slot
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QGraphicsScene, QGraphicsSceneMouseEvent

from Gui.colored_square import ColoredSquare
from Entity.human import Human


class GameScene(QGraphicsScene):
    def __init__(self, gameplay) -> None:
        super().__init__()
        self.gameplay = gameplay
        self.decalage_x: int = 0
        self.decalage_y: int = 0
        self.current_entity_selected: Human = None

        # timer to reset vue
        self.timer: QTimer = QTimer()
        self.timer.timeout.connect(self.update_vue)
        self.timer.start(200)

        self.entity: list = []

        self.gameplay.create_entity(0, 0)
        self.gameplay.create_entity(100, 0)

        self.squares = []
        self.update_vue()

        # Définir la taille de la scène sur une valeur très grande
        self.setSceneRect(QRectF(-10000, -10000, 20000, 20000))

    def create_entity(self, x: int, y: int) -> None:
        self.entity.append(Human(x + self.decalage_x, y + self.decalage_y))

    def update_vue(self) -> None:
        for square in self.squares:
            self.removeItem(square)  # Supprime chaque carré de la scène

        self.squares = []  # Réinitialise la liste des carrés

        for i in self.gameplay.entity:
            new_square = ColoredSquare(i.pos_x, i.pos_y, 50, Qt.red, i)
            new_square.clicked.connect(self.handle_square_click)

            self.squares.append(new_square)
            self.addItem(new_square)  # Ajoute les nouveaux carrés à la scène

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        item = self.itemAt(event.scenePos(), self.views()[0].transform())
        # if instance entity
        if isinstance(item, ColoredSquare):
            self.handle_square_click(item.entity)
        else:
            scene_pos = event.scenePos()
            message = f"Clic ailleurs dans la scène : x = {scene_pos.x() - self.decalage_x}, y = {scene_pos.y() - self.decalage_y}"
            print(message)
            if self.current_entity_selected:
                self.current_entity_selected.direction = \
                    (scene_pos.x() - self.decalage_x, scene_pos.y() - self.decalage_y)

    def handle_square_click(self, clicked_entity: Human) -> None:
        print(f"Carré rouge cliqué ! Appartient à l'entité : {clicked_entity.id}")
        self.current_entity_selected = clicked_entity
