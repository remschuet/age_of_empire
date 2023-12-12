import math

from PySide6.QtCore import QTimer
from Entity.entity import Entity
from Entity.human import Human
from Utils.math import is_collided
from common.const_resource import *


class Villager(Human):
    def __init__(self, player_name: str, x: int, y: int, get_entity_by_id, villager_action) -> None:
        super().__init__(player_name, x, y, get_entity_by_id)

        self.villager_action = villager_action
        self.type_resource = CONST_GOLD

    def action(self):
        if not self.tick % 2:
            self.mine_resource()

    def mine_resource(self):
        self.villager_action(self.id, self.type_resource)
