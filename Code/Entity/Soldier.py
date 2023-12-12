import math

from PySide6.QtCore import QTimer
from Entity.entity import Entity
from Entity.human import Human
from Utils.math import is_collided


class Soldier(Human):

    def __init__(self, player_name: str, x: int, y: int, get_entity_by_id) -> None:
        super().__init__(player_name, x, y, get_entity_by_id)

        self.__target: int = 0

    def action(self):
        if not self.tick % 2:
            self.attack()

    def attack(self):
        target_entity = self.get_entity_by_id(self.target)
        if target_entity:
            if (is_collided(self.pos_x, self.pos_y, self.size_x, self.size_y,
                            target_entity.pos_x, target_entity.pos_y, target_entity.size_x, target_entity.size_y)):
                print(f"-----Collision Detected:-----")
                target_entity.hp -= 1
            else:
                self.direction = (target_entity.pos_x + (target_entity.size_x / 2), target_entity.pos_y + (target_entity.size_y / 2))
        else:
            self.target = 0

    @property
    def target(self) -> int:
        return self.__target

    @target.setter
    def target(self, value: int):
        self.__target = value
