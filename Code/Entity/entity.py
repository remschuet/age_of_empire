from PySide6.QtCore import QTimer


class Entity:
    Entity_id = 0

    def __init__(self, player_name, x: int, y: int, get_entity_by_id) -> None:
        Entity.Entity_id += 1
        self.id = Entity.Entity_id
        self.player_name = player_name
        self.pos_x = x
        self.pos_y = y
        self.get_entity_by_id = get_entity_by_id

        self.alive = True
        self.hp = 1
        self.size_x = 20
        self.size_y = 20
        self.tick = 0

    def get_pos_xy(self) -> tuple:
        return self.pos_x, self.pos_y

