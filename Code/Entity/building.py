import math

from PySide6.QtCore import QTimer
from Entity.entity import Entity
from Utils.math import is_collided


class Building(Entity):

    def __init__(self, player_name: str, x: int, y: int, get_entity_by_id) -> None:
        super().__init__(player_name, x, y, get_entity_by_id)
        self.hp = 10
