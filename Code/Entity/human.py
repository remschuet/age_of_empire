import math

from PySide6.QtCore import QTimer
from Entity.entity import Entity


class Human(Entity):

    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y)

        # timer to move all element
        self.timer = QTimer()
        self.timer.timeout.connect(self.bouger)
        self.timer.start(2000)

        self.__direction: tuple = (x - 120, y - 40)
        self.__speed: int = 20

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

    @property
    def direction(self) -> tuple:
        return self.__direction

    @direction.setter
    def direction(self, value: tuple) -> None:
        self.__direction = value
