from Entity.entity import Entity
from Entity.human import Human


class Gameplay:
    def __init__(self):
        self.entity: list = []
        self.decalage_x: int = 0
        self.decalage_y: int = 0
        self.create_entity(0, 0)
        self.create_entity(100, 0)
        self.__current_entity_id: int = None

    @property
    def current_entity_id(self) -> int:
        return self.__current_entity_id

    @current_entity_id.setter
    def current_entity_id(self, entity: int) -> None:
        self.__current_entity_id = entity

    def create_entity(self, x: int, y: int) -> None:
        self.entity.append(Human(x + self.decalage_x, y + self.decalage_y))

    def click_screen(self, position: tuple):
        print(f"click : {position[0]} - {position[1]}")
        #if self.current_entity_selected:
           # self.current_entity_selected.direction = \
            #    (position[0], position[1])
                #( scene_pos.x() - self.gameplay.decalage_x, scene_pos.y() - self.gameplay.decalage_y)
