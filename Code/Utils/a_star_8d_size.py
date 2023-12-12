import heapq
import numpy as np


def AStar(grid, start_pos: tuple, goal_pos: tuple, obj_size: int = 2):
    start_pos = tuple(reversed(start_pos))
    goal_pos = tuple(reversed(goal_pos))

    rows, cols = grid.shape
    open_set = []
    closed_set = set()

    node_info = np.zeros((rows, cols, 5), dtype=int)

    start_row, start_col = start_pos
    goal_row, goal_col = goal_pos

    node_info[start_row, start_col, :] = [0, heuristic(start_pos, goal_pos), heuristic(start_pos, goal_pos), -1, -1]

    heapq.heappush(open_set, (node_info[start_row, start_col, 2], start_row, start_col))

    while open_set:
        _, current_row, current_col = heapq.heappop(open_set)
        current_node = node_info[current_row, current_col, :]

        if (current_row, current_col) == goal_pos:
            path = reconstruct_path(node_info, goal_pos)
            return path

        closed_set.add((current_row, current_col))

        for neighbor_row, neighbor_col in neighbors(current_row, current_col, rows, cols):
            if (neighbor_row, neighbor_col) in closed_set or grid[neighbor_row, neighbor_col] == 1:
                continue

            if obj_size == 2:
                value_above = 0
                value_right = 0
                value_below = 0
                value_left = 0
                #########################################
                # Affichage de la valeur de la cellule à gauche
                if neighbor_col > 0:
                    value_left = grid[neighbor_row, neighbor_col - 1]
                    # print("Gauche :", value_left)

                # Affichage de la valeur de la cellule à droite
                if neighbor_col < cols - 1:
                    value_right = grid[neighbor_row, neighbor_col + 1]
                    # print("Droite :", value_right)

                # Affichage de la valeur de la cellule au-dessus
                if neighbor_row > 0:
                    value_above = grid[neighbor_row - 1, neighbor_col]
                    # print("Dessus :", value_above)

                # Affichage de la valeur de la cellule en dessous
                if neighbor_row < rows - 1 and grid[neighbor_row + 1, neighbor_col] == 1:
                    value_below = grid[neighbor_row + 1, neighbor_col]
                    # print("Dessous :", value_below)

                if value_below == 1 or value_right == 1:
                    continue

                #########################################

            tentative_g_score = current_node[0] + 1

            if tentative_g_score < node_info[neighbor_row, neighbor_col, 0] or (neighbor_row, neighbor_col) not in [
                item[1:] for item in open_set]:
                node_info[neighbor_row, neighbor_col, :] = [tentative_g_score,
                                                            heuristic((neighbor_row, neighbor_col), goal_pos),
                                                            tentative_g_score + heuristic((neighbor_row, neighbor_col),
                                                                                          goal_pos), current_row,
                                                            current_col]
                heapq.heappush(open_set, (node_info[neighbor_row, neighbor_col, 2], neighbor_row, neighbor_col))

    return None


def heuristic(point1, point2):
    return np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

def heuristic(a, b):
    dx = abs(a[0] - b[0])
    dy = abs(a[1] - b[1])

    # Coût supplémentaire pour les déplacements diagonaux
    diagonal_cost = 1.4  # Cela peut être ajusté en fonction de vos préférences

    return (dx + dy) + (diagonal_cost - 2) * min(dx, dy)


def neighbors(row, col, rows, cols):
    valid_neighbors = []
    for i, j in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
        new_row, new_col = row + i, col + j
        if 0 <= new_row < rows and 0 <= new_col < cols:
            valid_neighbors.append((new_row, new_col))
    return valid_neighbors


def reconstruct_path(node_info, goal):
    path = []
    current = goal
    while current != (-1, -1):
        path.append(current[::-1])
        current = tuple(node_info[current[0], current[1], 3:])

    return list(reversed(path))


if __name__ == "__main__":
    grille = np.array(
    [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0]
    ]
    )

    start = (0, 0)
    goal = (7, 2)
    path = AStar(grille, start, goal)
    print("Chemin trouvé:", path)
