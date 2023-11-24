import math

from PySide6.QtCore import QTimer
from Entity.entity import Entity
from Utils.math import is_collided


class Human(Entity):

    def __init__(self, player_name: str, x: int, y: int, get_entity_by_id) -> None:
        super().__init__(player_name, x, y, get_entity_by_id)
        self.hp = 10

        # timer to move all element
        self.timer = QTimer()
        self.timer.timeout.connect(self.human_action)
        self.timer.start(250)

        self.__direction: tuple = (x - 120, y - 40)
        self.__speed: int = 10
        self.__target: int = 0

    def human_action(self) -> None:
        self.tick += 1
        if not self.tick % 2:
            self.bouger()
        if not self.tick % 2:
            self.attack()

    def bouger(self) -> None:
        if self.__direction is not None:
            # Calculer les composantes x et y du vecteur de déplacement
            dx = self.__direction[0] - self.pos_x
            dy = self.__direction[1] - self.pos_y

            # Calculer la distance entre la position actuelle et la destination
            distance = math.sqrt(dx ** 2 + dy ** 2)

            # Vérifier si la distance est suffisamment grande pour se déplacer
            if distance > self.__speed:
                # Calculer les composantes normalisées du vecteur de déplacement
                normalized_dx = dx / distance
                normalized_dy = dy / distance

                # Mettre à jour les positions
                self.pos_x += normalized_dx * self.__speed
                self.pos_y += normalized_dy * self.__speed
            else:
                # La destination est atteinte, vous pouvez ajuster cela en fonction de vos besoins
                self.pos_x = self.__direction[0]
                self.pos_y = self.__direction[1]

    def attack(self):
        target_entity = self.get_entity_by_id(self.target)
        if target_entity:
            if (is_collided(self.pos_x, self.pos_y, self.size, self.size,
                            target_entity.pos_x, target_entity.pos_y, target_entity.size, target_entity.size)):
                print(f"-----Collision Detected:-----")
                target_entity.hp -= 1
            else:
                self.direction = (target_entity.pos_x + (target_entity.size / 2), target_entity.pos_y + (target_entity.size / 2))
        else:
            self.target = 0

    @property
    def direction(self) -> tuple:
        return self.__direction

    @direction.setter
    def direction(self, value: tuple) -> None:
        self.__direction = value

    @property
    def target(self) -> int:
        return self.__target

    @target.setter
    def target(self, value: int):
        self.__target = value
