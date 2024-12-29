import heapq

input = """
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############"""


import os

input_file_path = os.path.join(os.path.dirname(__file__), "input.txt")
with open(input_file_path, "r") as f:
    input = f.read().strip()

HEIGHT = len(input.strip().split("\n"))
WIDTH = len(input.strip().split("\n")[0])

EXPLORABLE_SPACES = [".", "E"]

map = [["." for _ in range(WIDTH)] for _ in range(HEIGHT)]

for y, row in enumerate(input.strip().split("\n")):
    for x, item in enumerate(row.strip()):
        map[y][x] = item

        if item == "E":
            END_LOCATION = (x, y)
        if item == "S":
            START_LOCATION = (x, y)


def dikstra_solve(map):
    MOVEMENTS = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    queue = [(0, START_LOCATION)]
    visited = set()

    while queue:
        cost, location = heapq.heappop(queue)

        if location == END_LOCATION:
            return cost

        if location in visited:
            continue

        visited.add(location)

        for move in MOVEMENTS:
            dx, dy = move
            x, y = location

            if HEIGHT > y + dy >= 0 and WIDTH > x + dx >= 0:
                if map[y + dy][x + dx] in EXPLORABLE_SPACES and (x + dx, y + dy) not in visited:
                    heapq.heappush(queue, (cost + 1, (x + dx, y + dy)))


baseline = dikstra_solve(map)
print("baseline pico seconds:", baseline)


savings_over_100_counter = 0
for y in range(1, HEIGHT - 1):
    for x in range(1, WIDTH - 1):
        if map[y][x] == "#":

            # remove the wall
            map[y][x] = "."

            # solve the maze
            cheater_time = dikstra_solve(map)

            if baseline - cheater_time >= 100:
                print(f"removing ({x},{y}) makes it solvable in {cheater_time}, saving {baseline - cheater_time}")
                savings_over_100_counter += 1

            # put the wall back
            map[y][x] = "#"

print(f"there are {savings_over_100_counter} cheats to save at least 100 picoseconds")
