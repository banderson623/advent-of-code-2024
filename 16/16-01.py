import heapq
from time import sleep

input = """
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############"""

# input = """
# #################
# #...#...#...#..E#
# #.#.#.#.#.#.#.#.#
# #.#.#.#...#...#.#
# #.#.#.#.###.#.#.#
# #...#.#.#.....#.#
# #.#.#.#.#.#####.#
# #.#...#.#.#.....#
# #.#.#####.#.###.#
# #.#.#.......#...#
# #.#.###.#####.###
# #.#.#...#.....#.#
# #.#.#.#####.###.#
# #.#.#.........#.#
# #.#.#.#########.#
# #S#.............#
# #################"""

# input = """
# #########################
# #...#.......#.#.#.#...#.#
# #.#######.#.#.###.#.#.#.#
# #.........#.#.#...#.#.#.#
# #####.###.#.#.#.###.#.###
# #...#.#.....#.#.#...#...#
# #.#.#.#.#.#.#.#.#.###.###
# #E#...#...#...#.#.#...#.#
# #.#######.#.###.#.#.###.#
# #.#...#...#.....#.#...#.#
# #.#.#.#.###.#####.###.###
# #...#.#.#...#.....#.....#
# #######.#.#.#.#####.#####
# #.....#.#.#...#...#...#.#
# #.###.#.#.#.#####.###.#.#
# #...#...#.#.#.......#.#.#
# #.#.#.###.#.#.###.###.###
# #.#.#.#...#...#...#.....#
# ###.#.#.###.###.###.#####
# #...#.#.....#.....#.....#
# #.#########.#.#####.###.#
# #...........#.#...#...#.#
# #.#######.#####.#.#####.#
# #.......#.......#.....#.#
# #######.#.#.#########.#.#
# #.....#.....#.....#...#.#
# #####.###.###.###.#.###.#
# #.....#...#...#.#.#.#...#
# #.#####.#.#.###.#.#.#####
# #S......#.......#.......#
# #########################"""

# import os

# input_file_path = os.path.join(os.path.dirname(__file__), "input.txt")
# with open(input_file_path, "r") as f:
#     input = f.read().strip()

HEIGHT = len(input.strip().split("\n"))
WIDTH = len(input.strip().split("\n")[0])

EXPLORABLE_SPACES = [".", "E"]

# MOVEMENTS = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}
MOVEMENTS = [(0, -1), (1, 0), (0, 1), (-1, 0)]
DIRECTION_NAMES = ["N", "E", "S", "W"]
DIRECTION_SYMBOLS = ["^", ">", "v", "<"]
# DIRECTIONS = list(MOVEMENTS.keys())
START_DIRECTION = 1

map = [["." for _ in range(WIDTH)] for _ in range(HEIGHT)]

start_location = None
end_location = None

for y, row in enumerate(input.strip().split("\n")):
    for x, item in enumerate(row.strip()):
        map[y][x] = item

        if item == "E":
            end_location = (x, y)
        if item == "S":
            start_location = (x, y)


def prettyPrint(map, other_location=None):
    if other_location:
        map[other_location[1]][other_location[0]] = "*"

    for row in map:
        print("".join(row))


def dijkstra_solver(map, start_location, end_location):
    # Priority queue: (cost, location, direction)
    queue = [(0, start_location, START_DIRECTION)]
    visited = set()
    journey = {}

    while queue:
        # this queue will always return the lowest cost option as the next one
        # which allows me to continue to explore the map advancing the cheapest one next
        # ...
        # and we only add steps to explore if:
        #  1. "foward" is a valid space, that hasn't been visited
        #  2. rotating left
        #  3. rotating right
        cost, location, direction = heapq.heappop(queue)
        x, y = location

        # map[y][x] = DIRECTION_SYMBOLS[direction]
        # prettyPrint(map)
        # sleep(0.1)

        if location == end_location:
            return cost

        if (x, y, direction) in visited:
            continue

        visited.add((x, y, direction))

        # Straight ahead
        dx, dy = MOVEMENTS[direction]
        next_x = x + dx
        next_y = y + dy

        if map[next_y][next_x] in EXPLORABLE_SPACES:
            journey[(next_x, next_y, direction)] = (x, y, direction)
            heapq.heappush(queue, (cost + 1, (next_x, next_y), direction))

        # Rotate LEFT to explore
        left = (direction - 1) % len(MOVEMENTS)
        if (x, y, left) not in visited:
            dx, dy = MOVEMENTS[left]
            if map[y + dy][x + dx] in EXPLORABLE_SPACES:
                heapq.heappush(queue, (cost + 1000, (x, y), left))

        # rotate RIGHT to explore
        right = (direction + 1) % len(MOVEMENTS)
        if (x, y, right) not in visited:
            dx, dy = MOVEMENTS[right]
            if map[y + dy][x + dx] in EXPLORABLE_SPACES:
                heapq.heappush(queue, (cost + 1000, (x, y), right))

    print(f"I couldn't find a way to the end")
    return -1


cost = dijkstra_solver(map, start_location, end_location)
print(cost)
