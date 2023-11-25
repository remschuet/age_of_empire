from Entity.entity import Entity


class TownCenter(Entity):
    def __init__(self, player_name: str, x: int, y: int, get_entity_by_id) -> None:
        super().__init__(player_name, x, y, get_entity_by_id)
        self.hp = 10
        self.size_x: int = 120
        self.size_y: int = 80
