from PySide6.QtCore import QTimer


class Entity:
    Entity_id = 0

    def __init__(self, x: int, y: int) -> None:
        Entity.Entity_id += 1
        self.id = Entity.Entity_id
        self.pos_x = x
        self.pos_y = y
