import numpy as np

from Utils.a_star import astar

"""
- point : (d, y) in size_map
- position : 0, 1, 2, ... size_map
"""


class GameNumpy:
    def __init__(self, size_map, size_case):
        self.__size_map = size_map
        self.__size_case = size_case
        self.__array_map = np.zeros((int(self.__size_map / self.__size_case), int(self.__size_map / self.__size_case)))

    @property
    def array_map(self) -> np.ndarray:
        return self.array_map

    def get_arr_coords_from_position(self, position: tuple) -> tuple:
        return position[0] / self.__size_case, position[1] / self.__size_case

    def set_point(self, point: tuple, value: int) -> None:
        self.__size_map[point[0]][1] = value

    def get_path(self, start_pos: tuple, end_pos: tuple) -> np.ndarray:
        """ documentation
        :param start_pos: tuple (x, y)
        :param end_pos: tuple (x, y)
        :return path [[x, y], [x, y]], np.ndarray
        """

        """Obtient le chemin entre deux positions.

        Args:
            start_pos (tuple): Position de départ au format (x, y).
            end_pos (tuple): Position de fin au format (x, y).

        Returns:
            np.ndarray: Tableau NumPy représentant le chemin au format [[x, y], [x, y]].
        """

        path: np.ndarray = astar(self.__array_map, start_pos, end_pos)
        return path
