import heapq

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(start, goal, grid):
    rows, cols = len(grid), len(grid[0])
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    def is_valid(x, y):
        return 0 <= x < rows and 0 <= y < cols and grid[x][y] == 0

    open_set = []
    closed_set = set()

    heapq.heappush(open_set, (0, start))

    while open_set:
        current_cost, current_node = heapq.heappop(open_set)

        if current_node == goal:
            return True  # Goal atteint

        closed_set.add(current_node)

        for dx, dy in directions:
            neighbor = (current_node[0] + dx, current_node[1] + dy)

            if is_valid(*neighbor) and neighbor not in closed_set:
                new_cost = current_cost + 1 + heuristic(neighbor, goal)
                heapq.heappush(open_set, (new_cost, neighbor))

    return False  # A* n'a pas trouvé de chemin

# Exemple d'utilisation
grid_example = [
    [0, 0, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0]
]

start_point_example = (0, 0)
goal_point_example = (4, 4)

result = astar(start_point_example, goal_point_example, grid_example)
print(result)
