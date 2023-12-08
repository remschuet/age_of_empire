import numpy as np
from Utils.a_star import AStar
from typing import Optional

class GameNumpy:
    """ 2D game world using NumPy arrays to represent location of objets

        TERMINOLOGY  : use for this class

        - point         : type: int
                        : possibility of range(0, size_map / size_case)
                        : tuple data accept: (x, y)

        - position      : type: int or float
                        : possibility of range(0, size_map)
                        : tuple data accept: (x, y)

        OTHER        : use for this class

        array_map       : type: int
                        : range(0, size_map / size_case)
                        : data access array_map[y][x]
                        : data by cells [0 = empty, 1 = full]

    """

    def __init__(self, size_map: int, size_case: int):
        """
        :param size_map: The size of the game world (square)
        :param size_case: The size of each grid cell in the view
        """
        self.__size_map: int = size_map
        self.__size_case: int = size_case

        self.__array_map: np.ndarray
        self.__set_array_map_zero()

    @property
    def array_map(self) -> np.ndarray:
        return self.__array_map

    def __set_array_map_zero(self):
        self.__array_map = np.zeros((int(self.__size_map / self.__size_case),
                                     int(self.__size_map / self.__size_case)))

    def get_points_from_position(self, position: tuple[float, float]) -> tuple[int, int]:
        """
        :param      position: (x, y)
        :return:    point (x, y)
        """
        return int(position[0] / self.__size_case), int(position[1] / self.__size_case)

    def set_point_rect(self, point: tuple, width: int, height: int, value: int) -> None:
        """
        :param point: [(x, y), (x, y)]
        :param width: size of the shape, size in format point
        :param height size of the shape, size in format point
        :param value: 0 = empty, 1 = full
        """
        points: list[tuple] = []
        x, y = point
        for w in range(width):
            for h in range(height):
                points.append((x + w, y + h))
        self.set_points(points, value)

    def set_points(self, points: list[tuple], value: int) -> None:
        """
        :param points: [(x, y), (x, y)]
        :param value: 0 = empty, 1 = full
        """
        for point in points:
            self.set_point(point, value)

    def set_point(self, point: tuple[int, int], value: int) -> None:
        """
        :param point: (x, y)
        :param value: 0 = empty, 1 = full
        """
        self.__array_map[point[1]][point[0]] = value

    def get_path_relative(self, start_position: tuple[int, int], end_position: tuple[int, int]):
        """ Get shorts path (position) between 2 points in a 2d matrices
        :param start_position: format (x, y)
        :param end_position:   format (x, y)

        :return: path using this format : [[x, y], [x, y]].
        :rtype: np.ndarray or None
        """

        x_reste = int(start_position[0] % self.__size_case)
        y_reste = int(start_position[1] % self.__size_case)

        start_point = self.get_points_from_position(start_position)
        end_point = self.get_points_from_position(end_position)

        path: list[tuple] = AStar(self.__array_map, start_point, end_point)
        path_relative = [(x * self.__size_case + x_reste, y * self.__size_case + y_reste) for x, y in path]
        path_relative.append(end_position)

        return path_relative

    def get_path(self, start_point: tuple[int, int], end_point: tuple[int, int]) -> np.ndarray:
        """ Get shorts path (point) between 2 points in a 2d matrices

        :param start_point: format (x, y)
        :param end_point:   format (x, y)

        :return: path using this format : [[x, y], [x, y]].
        :rtype: np.ndarray or None

        :raises path = None: If no path found, return None.
        """

        path: np.ndarray = AStar(self.__array_map, start_point, end_point)
        return path


if __name__ == "__main__":
    game_np = GameNumpy(400, 20)
    game_np.set_point((5, 10), 1)
    array = game_np.array_map
    print(array)
    pos = game_np.get_points_from_position((20, 79))
    print(pos)
    pos = game_np.get_path((2, 4), (2, 8))
    print(pos)
    pos = game_np.get_path_relative((22, 44), (46, 88))
    print(pos)
