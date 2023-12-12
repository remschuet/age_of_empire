import sys
from PySide6.QtWidgets import QGraphicsRectItem, QGraphicsSceneMouseEvent, QApplication, QGraphicsScene, QGraphicsRectItem, QGraphicsView, QVBoxLayout, QWidget, QLabel
from PySide6.QtCore import Qt, QRectF, QTimerEvent, QTimer, Slot, Signal, QObject

from Serveur.client import *

game_scene = None


class ColoredSquare(QGraphicsRectItem, QObject):
    clicked = Signal(object)  # Le signal peut transporter un objet (dans ce cas, l'entité associée)

    def __init__(self, x, y, size, color, entity):
        super().__init__(x, y, size, size)
        self.setBrush(color)
        self.pos_x = x
        self.pos_y = y
        self.entity = entity

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        if self.brush().color() == Qt.red:
            self.clicked.emit(self.entity)


class Human():
    HumanId = 0

    def __init__(self, x, y):
        Human.HumanId += 1
        self.id = Human.HumanId
        self.pos_x = x
        self.pos_y = y

        self._rel_x = x
        self._rel_y = y

        # Créer un timer pour mettre à jour la vue toutes les 20 millisecondes
        self.timer = QTimer()
        self.timer.timeout.connect(self.bouger)
        self.timer.start(2000)

    def bouger(self):
        self.pos_x += 20
        self._rel_x += 20


class GameScene(QGraphicsScene):
    def __init__(self):
        super().__init__()

        self.decalage_x = 0
        self.decalage_y = 0

        # Créer un timer pour mettre à jour la vue toutes les 20 millisecondes
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_vue)
        self.timer.start(2000)

        self.entity = []

        self.create_entity(0, 0)
        self.create_entity(100, 0)

        self.squares = []
        self.update_vue()

        # Définir la taille de la scène sur une valeur très grande
        self.setSceneRect(QRectF(-10000, -10000, 20000, 20000))

    def create_entity(self, x, y):
        self.entity.append(Soldier(x + self.decalage_x, y + self.decalage_y))

    def update_vue(self):
        for square in self.squares:
            self.removeItem(square)  # Supprime chaque carré de la scène

        self.squares = []  # Réinitialise la liste des carrés

        for i in self.entity:
            new_square = ColoredSquare(i.pos_x, i.pos_y, 50, Qt.red, i)
            new_square.clicked.connect(self.handle_square_click)

            self.squares.append(new_square)
            self.addItem(new_square)  # Ajoute les nouveaux carrés à la scène

    def handle_square_click(self, clicked_entity):
        print(f"Carré rouge cliqué ! Appartient à l'entité : {clicked_entity.id}")

class GameView(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)
        self.move_x = 0
        self.move_y = 0

        # Activer la réception des événements clavier
        self.setFocusPolicy(Qt.StrongFocus)

        # Désactiver les barres de défilement
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def move_element(self):
        for enti in self.scene().entity:
            enti.pos_x += self.move_x
            enti.pos_y += self.move_y

    def keyPressEvent(self, event):
        step = 10  # Ajustez la taille du pas selon vos besoins
        if event.key() == Qt.Key_Left:
            self.move_x += step
            self.scene().decalage_x += 10
        elif event.key() == Qt.Key_Right:
            self.move_x -= step
            self.scene().decalage_x -= 10
        elif event.key() == Qt.Key_Up:
            self.move_y += step
            self.scene().decalage_y += 10
        elif event.key() == Qt.Key_Down:
            self.scene().decalage_y -= 10
            self.move_y -= step

        self.move_element()
        self.scene().update_vue()
        self.move_x = 0
        self.move_y = 0


def handle_event(message):
    global game_scene
    data = message.split(";")
    if data[0] == "entity":
        game_scene.create_entity(int(data[1]), int(data[2]))  # Convertir les chaînes en entiers
    else:
        print(f"Received message from client: {message}")


def main():
    global game_scene
    app = QApplication(sys.argv)
    game_scene = GameScene()

    # Client part
    client = Client()
    client.eventTriggered.connect(handle_event)

    # Créer une scène de jeu
    # Créer une vue personnalisée pour afficher la scène
    game_view = GameView(game_scene)

    # Créer un widget pour le QLabel
    label_widget = QLabel("Hello, World!")

    # Créer un layout vertical
    layout = QVBoxLayout()
    layout.addWidget(game_view)
    layout.addWidget(label_widget)

    # Créer un widget principal pour contenir le layout
    main_widget = QWidget()
    main_widget.setLayout(layout)

    # Afficher le widget principal
    main_widget.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()