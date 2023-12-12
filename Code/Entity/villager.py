from Entity.human import Human
from common.const_resource_entity import *


class Villager(Human):
    SIZE_X = 20
    SIZE_Y = 40

    def __init__(self, player_name: str, x: int, y: int, get_entity_by_id, villager_action) -> None:
        super().__init__(player_name, x, y, get_entity_by_id)

        self.villager_action = villager_action
        self.type_resource = CONST_GOLD
        self.qty = 10
        self.size_x = 15
        self.size_y = 30

    def action(self):
        if not self.tick % 10:
            self.mine_resource()

    def mine_resource(self):
        self.villager_action(self.player_name, self.type_resource, self.qty)
