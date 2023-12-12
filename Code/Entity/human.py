import math

from PySide6.QtCore import QTimer
from Entity.entity import Entity
from Utils.math import is_collided


class Human(Entity):
    SIZE_X = 40
    SIZE_Y = 40

    def __init__(self, player_name: str, x: int, y: int, get_entity_by_id) -> None:
        super().__init__(player_name, x, y, get_entity_by_id)
        self.hp = 10

        # timer to move all element
        self.timer = QTimer()
        self.timer.timeout.connect(self.human_action)
        self.timer.start(250)

        self.__direction: tuple = None
        self.__direction_list: list[tuple] = []

        self.__speed: int = 10
        self.size_x = 40
        self.size_y = 40

    def human_action(self) -> None:
        self.tick += 1
        if not self.tick % 2:
            self.bouger()
        self.action()

    # for children
    def action(self):
        pass

    def __get_next_direction(self):
        if self.__direction_list and self.__direction_list[0] is not None:
            self.__direction = self.__direction_list[0]
            self.__direction_list.pop(0)

    def bouger(self) -> None:
        if self.__direction is None:
            self.__get_next_direction()
        else:
            if self.__direction[0] == self.pos_x and self.__direction[1] == self.pos_y:
                self.__get_next_direction()
            # Calculer les composantes x et y du vecteur de déplacement
            dx = self.__direction[0] - self.pos_x
            dy = self.__direction[1] - self.pos_y

            # print("direction : ", self.__direction[0], " - ", self.__direction[1], " pos : " self.pos_x and self.__direction[1] == self.pos_y)
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

    @property
    def direction(self) -> tuple:
        return self.__direction

    @direction.setter
    def direction(self, value: tuple) -> None:
        self.__direction = value

    @property
    def direction_list(self) -> list:
        return self.__direction_list

    @direction_list.setter
    def direction_list(self, value: list) -> None:
        print(value)
        self.__direction_list = value
