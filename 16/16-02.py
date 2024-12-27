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

input = """
#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################"""

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

import os

input_file_path = os.path.join(os.path.dirname(__file__), "input.txt")
with open(input_file_path, "r") as f:
    input = f.read().strip()

HEIGHT = len(input.strip().split("\n"))
WIDTH = len(input.strip().split("\n")[0])

EXPLORABLE_SPACES = [".", "E"]

MOVEMENTS = [(0, -1), (1, 0), (0, 1), (-1, 0)]
DIRECTION_NAMES = ["N", "E", "S", "W"]
DIRECTION_SYMBOLS = ["^", ">", "v", "<"]
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
    queue = [(0, start_location, START_DIRECTION, set())]
    visited = {}
    winning_path_locations = set()

    lowest_cost = None

    while queue:
        # this queue will always return the lowest cost option as the next one
        # which allows me to continue to explore the map advancing the cheapest one next
        # ...
        # and we only add steps to explore if:
        #  1. "foward" is a valid space, that hasn't been visited
        #  2. rotating left
        #  3. rotating right
        cost, location, direction, path = heapq.heappop(queue)
        x, y = location

        # the first lowest cost path will get to the end first,
        # and set the lowest cost

        # We still want to consider other paths that are the same cost
        # ...  multiple times we can only consider the lowest cost paths
        if lowest_cost is not None and cost > lowest_cost:
            continue

        if location == end_location:
            print(f"Found the end at {location} with a cost of {cost} and steps {len(path)}")

            lowest_cost = cost
            path.add((x, y, DIRECTION_NAMES[direction]))

            for px, py, _ in path:
                winning_path_locations.add((px, py))

            continue

        # we don't continue if the cost is the same, because it allows for an alternate path
        # of the same cost to be explored.
        if (x, y, direction) in visited and visited[(x, y, direction)] > cost:
            continue

        visited[(x, y, direction)] = cost

        # Straight ahead
        dx, dy = MOVEMENTS[direction]
        next_x = x + dx
        next_y = y + dy

        if map[next_y][next_x] in EXPLORABLE_SPACES:
            updated_path = path.copy()
            updated_path.add((x, y, DIRECTION_NAMES[direction]))
            heapq.heappush(queue, (cost + 1, (next_x, next_y), direction, updated_path))

        # Rotate LEFT to explore
        left = (direction - 1) % len(MOVEMENTS)
        if (x, y, left) not in visited:
            dx, dy = MOVEMENTS[left]
            if map[y + dy][x + dx] in EXPLORABLE_SPACES:
                heapq.heappush(queue, (cost + 1000, (x, y), left, path))

        # rotate RIGHT to explore
        right = (direction + 1) % len(MOVEMENTS)
        if (x, y, right) not in visited:
            dx, dy = MOVEMENTS[right]
            if map[y + dy][x + dx] in EXPLORABLE_SPACES:
                heapq.heappush(queue, (cost + 1000, (x, y), right, path))

    # how many seats are there to watch the winning paths?
    return winning_path_locations


great_seats = dijkstra_solver(map, start_location, end_location)

# Reset the map and show only good seats
map = [[" " for _ in range(WIDTH)] for _ in range(HEIGHT)]
for seat in great_seats:
    x, y = seat
    map[y][x] = "O"
prettyPrint(map)

print(len(great_seats))
