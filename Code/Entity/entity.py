from PySide6.QtCore import QTimer


class Entity:
    Entity_id = 0

    def __init__(self, player_name, x: int, y: int) -> None:
        Entity.Entity_id += 1
        self.id = Entity.Entity_id
        self.player_name = player_name
        self.pos_x = x
        self.pos_y = y
        self.alive = True
        self.hp = 1
        self.size = 50
        self.tick = 0

