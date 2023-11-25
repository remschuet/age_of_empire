import math

from PySide6.QtCore import QTimer
from Entity.entity import Entity
from Utils.math import is_collided


class Tower(Entity):
    def __init__(self, player_name: str, x: int, y: int, get_entity_by_id) -> None:
        super().__init__(player_name, x, y, get_entity_by_id)
        self.hp = 50

        # timer to move all element
        self.timer = QTimer()
        self.timer.timeout.connect(self.tower_action)
        self.timer.start(250)

        self.size_x = 20
        self.size_y = 40

        self.__distance_shooting = 50

        self.__target: int = 0

    def tower_action(self) -> None:
        self.tick += 1
        if not self.tick % 2:
            self.attack()

    def attack(self):
        target_entity = self.get_entity_by_id(self.target)
        if target_entity:
            if (is_collided(self.pos_x - self.__distance_shooting, self.pos_y - self.__distance_shooting,
                            self.size_x + self.__distance_shooting, self.size_y + self.__distance_shooting,
                            target_entity.pos_x, target_entity.pos_y, target_entity.size_x, target_entity.size_y)):
                print(f"-----Collision Detected:-----")
                target_entity.hp -= 1
        else:
            self.target = 0

    @property
    def target(self) -> int:
        return self.__target

    @target.setter
    def target(self, value: int):
        self.__target = value
