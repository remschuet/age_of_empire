from Entity.human import Human


class Gameplay:
    def __init__(self):
        self.entity: list = []
        self.decalage_x: int = 0
        self.decalage_y: int = 0

        pass

    def create_entity(self, x: int, y: int) -> None:
        self.entity.append(Human(x + self.decalage_x, y + self.decalage_y))
