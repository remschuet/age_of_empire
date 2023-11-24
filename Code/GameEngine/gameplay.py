from PySide6.QtCore import Signal, QObject, Slot, QTimer

from Entity.entity import Entity
from Entity.human import Human
from GameEngine.const_action import *


class Gameplay(QObject):
    action = Signal(str)

    def __init__(self, client_id):
        super().__init__()
        self.client_id = client_id

        self.entity: list = []
        self.decalage_x: int = 0
        self.decalage_y: int = 0
        self.received_create_entity(self.client_id, 0, 0)
        self.received_create_entity(self.client_id, 100, 0)
        self.__current_entity_id: int = None
        self.__current_action = ACTION_NULL

        # timer to move all element
        self.timer = QTimer()
        self.timer.timeout.connect(self.boucle)
        self.timer.start(500)

    @property
    def current_entity_id(self) -> int:
        return self.__current_entity_id

    @current_entity_id.setter
    def current_entity_id(self, entity: int) -> None:
        self.__current_entity_id = entity

    def boucle(self):
        # if entity are dead
        for ent in self.entity:
            if ent.hp < 0 or not ent.alive:
                self.entity.remove(ent)
                del ent

    def click_entity(self, id):
        entity_obj: Human = next((rect for rect in self.entity if rect.id == id), None)
        if entity_obj.player_name == self.client_id:
            self.__current_entity_id = id
        else:
            if self.__current_entity_id:
                self.emit_action_human_attack(self.__current_entity_id, id)
                my_human: Human = next((rect for rect in self.entity if rect.id == self.__current_entity_id), None)
                my_human.target = entity_obj
            else:
                print("Erreur attack, no current_entity_id")

    def click_screen(self, event):
        scene_pos = event.scenePos()
        if self.__current_action != ACTION_NULL:
            self.emit_action_create_human(event)
            self.__current_action = ACTION_NULL

        if self.current_entity_id and self.current_entity_id >= 1:
            entity_obj: Entity = next((rect for rect in self.entity if rect.id == self.current_entity_id), None)

            self.action.emit(f"{self.client_id};bouger;{entity_obj.id};"
                             f"{scene_pos.x() - self.decalage_x};"
                             f"{scene_pos.y() - self.decalage_y}")
            # self.current_entity_id = None

    def emit_action_human_attack(self, my_human_id: int, en_entity_id: int):
        self.action.emit(f"{self.client_id};attack;"
                         f"{int(my_human_id)};"
                         f"{int(en_entity_id)}")

    def emit_action_create_human(self, event):
        scene_pos = event.scenePos()
        self.action.emit(f"{self.client_id};entity;"
                         f"{int(scene_pos.x() - self.decalage_x)};"
                         f"{int(scene_pos.y() - self.decalage_y)}")

    @Slot()
    def received_action(self, action: int):
        self.__current_action = action

    @Slot()
    def received_direction_entity(self, id: int, pos_x: float, pos_y: float):
        entity_obj: Human = next((rect for rect in self.entity if rect.id == id), None)
        entity_obj.direction = (pos_x, pos_y)

    @Slot()
    def received_human_attack(self, attack_human_id: int, victim_entity_id: int):
        print("attack")
        attack_human: Human = next((rect for rect in self.entity if rect.id == attack_human_id), None)
        victim_entity: Entity = next((rect for rect in self.entity if rect.id == victim_entity_id), None)
        attack_human.target = victim_entity

    @Slot()
    def received_create_entity(self, player_name: str, x: int, y: int) -> None:
        self.entity.append(Human(player_name, x + self.decalage_x, y + self.decalage_y))
