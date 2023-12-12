CONST_GOLD = "gold"
CONST_WOOD = "wood"
CONST_ROCK = "rock"
CONST_FOOD = "food"


class AutoNumber:
    __counter = 0

    def __new__(cls):
        cls.__counter += 1
        return cls.__counter


CONST_NONE = AutoNumber()
CONST_VILLAGER = AutoNumber()
CONST_SOLDIER = AutoNumber()

CONST_TOWN_CENTER = AutoNumber()
CONST_TOWER = AutoNumber()
CONST_WALL = AutoNumber()

"""
from enum import Enum, auto

class EntityType(Enum):
    NONE = auto()
    VILLAGER = auto()
    SOLDIER = auto()
    TOWN_CENTER = auto()
    TOWER = auto()
    WALL = auto()

# Exemple d'utilisation :
print(EntityType.VILLAGER.value)  # Output: 2
print(EntityType.TOWER.value)     # Output: 5

"""