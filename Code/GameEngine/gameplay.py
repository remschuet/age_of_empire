from PySide6.QtCore import Signal, QObject, Slot, QTimer

from Entity.entity import Entity
from Entity.Soldier import Soldier
from Entity.human import Human
from Entity.tower import Tower
from Entity.town_center import TownCenter
from Entity.villager import Villager
from Entity.wall import Wall
from common.const_action import *
from common.const_resource import *
from GameEngine.game_numpy import GameNumpy


class Gameplay(QObject):
    action = Signal(str)
    evt_resource = Signal(dict)

    def __init__(self, client_id):
        super().__init__()
        self.client_id = client_id

        self.__size_map = 2000
        self.__size_case = 20
        self.__game_numpy = GameNumpy(self.__size_map, self.__size_case)

        self.entity: list = []
        self.decalage_x: int = 0
        self.decalage_y: int = 0

        self.__resource = {CONST_GOLD: 0,
                           CONST_FOOD: 0,
                           CONST_WOOD: 0,
                           CONST_ROCK: 0}

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

    # use by entity to get access to other entity
    def get_entity_by_id(self, id: int):
        entity_obj: Soldier = next((rect for rect in self.entity if rect.id == id), None)
        return entity_obj

    # use by villager to add some resource
    def villager_action(self, player_entity, type_resource: str, qty: int) -> None:  # type_resource = common/const_resources
        if player_entity == self.client_id:
            self.__resource[type_resource] += qty
            self.evt_resource.emit(self.__resource)

    def click_entity(self, id):
        entity_obj: Soldier = next((rect for rect in self.entity if rect.id == id), None)
        if entity_obj.player_name == self.client_id:
            self.__current_entity_id = id
        else:
            if self.__current_entity_id:
                self.emit_action_entity_attack(self.__current_entity_id, id)
            else:
                print("Erreur attack, no current_entity_id")

    # select or attack
    def click_screen(self, event):
        scene_pos = event.scenePos()
        if self.__current_action != ACTION_NULL:
            self.emit_action_create_entity(event)
            self.__current_action = ACTION_NULL

        if self.current_entity_id and self.current_entity_id >= 1:
            entity_obj: Entity = next((rect for rect in self.entity if rect.id == self.current_entity_id), None)
            self.emit_action_entity_move(entity_obj, scene_pos)

    @Slot()
    def boucle(self):
        # if entity are dead
        for ent in self.entity:
            if ent.hp < 0 or not ent.alive:
                if isinstance(ent, TownCenter) and ent.player_name == self.client_id:
                    self.emit_end_game()
                self.entity.remove(ent)
                del ent

    ###################################
    #######     SERVER PART     #######
    ###################################

    def received_from_server(self, message: str) -> None:
        # currently in game
        data = message.split(";")
        action = int(data[1])
        if action:
            if action == ACTION_PLACE_HUMAN:
                self.received_create_soldier(data[0], int(data[2]), int(data[3]))
            elif action == ACTION_PLACE_VILLAGER:
                self.received_create_villager(data[0], int(data[2]), int(data[3]))
            elif action == ACTION_PLACE_TOWER:
                self.received_create_tower(data[0], int(data[2]), int(data[3]))
            elif action == ACTION_MOVE_ENTITY:
                self.received_direction_entity(int(data[2]), int(float(data[3])), int(float(data[4])))
            elif action == ACTION_ATTACK:
                self.received_human_attack(int(data[2]), int(data[3]))
            elif action == ACTION_PLACE_TOWN_CENTER:
                self.received_create_town_center(data[0], int(data[2]), int(data[3]))
            elif action == ACTION_PLACE_WALL:
                self.received_create_wall(data[0], int(data[2]), int(data[3]))

    ###################################
    #######   CALL BY PLAYER    #######
    ###################################

    def emit_create_town_center(self, is_starter: bool) -> None:
        if is_starter:
            self.action.emit(f"{self.client_id};{ACTION_PLACE_TOWN_CENTER};"
                             f"{900};{920}")
        else:
            self.action.emit(f"{self.client_id};{ACTION_PLACE_TOWN_CENTER};{1100};{1200}")

    def emit_action_entity_move(self, entity_obj, scene_pos):
        self.action.emit(f"{self.client_id};{ACTION_MOVE_ENTITY};{entity_obj.id};"
                         f"{scene_pos.x() - self.decalage_x};"
                         f"{scene_pos.y() - self.decalage_y}")

    def emit_action_entity_attack(self, my_human_id: int, en_entity_id: int):
        self.action.emit(f"{self.client_id};{ACTION_ATTACK};"
                         f"{int(my_human_id)};"
                         f"{int(en_entity_id)}")

    def emit_action_create_entity(self, event):
        scene_pos = event.scenePos()
        self.__current_entity_id = 0
        print(self.__current_action)

        if self.__current_action == ACTION_PLACE_HUMAN:
            if self.__resource[CONST_GOLD] >= Soldier.PRICE:
                 # FIX ME dans un get pour remettre la vue
                self.__resource[CONST_GOLD] -= Soldier.PRICE
            else:
                return
        self.action.emit(f"{self.client_id};{self.__current_action};"
                         f"{int(scene_pos.x() - self.decalage_x)};"
                         f"{int(scene_pos.y() - self.decalage_y)}")

    def emit_end_game(self):
        self.action.emit(f"{self.client_id};{ACTION_END_GAME}")

    ###################################
    ######    CALL BY SERVER    #######
    ###################################

    @Slot()
    def received_action(self, action: int):
        self.__current_action = action

    @Slot()
    def received_direction_entity(self, id: int, pos_x: int, pos_y: int):
        entity_obj: Human = next((rect for rect in self.entity if rect.id == id), None)
        # entity_obj.direction = (pos_x, pos_y)
        np_path = self.__game_numpy.get_path_relative(entity_obj.get_pos_xy(), (pos_x, pos_y))
        entity_obj.direction_list = np_path
        # entity_obj.direction = (pos_x, pos_y)

    @Slot()
    def received_human_attack(self, attack_human_id: int, victim_entity_id: int):
        attack_human: Soldier = next((rect for rect in self.entity if rect.id == attack_human_id), None)
        attack_human.target = victim_entity_id

    @Slot()
    def received_create_soldier(self, player_name: str, x: int, y: int) -> None:
        self.entity.append(Soldier(player_name, x + self.decalage_x, y + self.decalage_y, self.get_entity_by_id))

    @Slot()
    def received_create_villager(self, player_name: str, x: int, y: int) -> None:
        self.entity.append(Villager(player_name, x + self.decalage_x, y + self.decalage_y, self.get_entity_by_id, self.villager_action))

    @Slot()
    def received_create_town_center(self, player_name: str, x: int, y: int) -> None:
        self.entity.append(TownCenter(player_name, x + self.decalage_x, y + self.decalage_y, self.get_entity_by_id))

    @Slot()
    def received_create_tower(self, player_name: str, x: int, y: int) -> None:
        self.entity.append(Tower(player_name,
                                 x + self.decalage_x - Tower.SIZE_X / 2,
                                 y + self.decalage_y - Tower.SIZE_Y / 2,
                                 self.get_entity_by_id))

    @Slot()
    def received_create_wall(self, player_name: str, x: int, y: int) -> None:
        # create wall
        pos_x = int((x + self.decalage_x) / self.__size_case)
        pos_y = int((y + self.decalage_y) / self.__size_case)
        self.entity.append(Wall(player_name, pos_x * 20, pos_y * 20, self.get_entity_by_id))
        # add to numpy array
        pos_x_in_array = int((x + self.decalage_x) / self.__size_case)
        pos_y_in_array = int((y + self.decalage_y) / self.__size_case)
        self.__game_numpy.set_point_rect((pos_x_in_array, pos_y_in_array), int(80 / 20), int(20 / 20), 1)

    @Slot()
    def received_end_game(self, loser_client_id: str):
        pass
