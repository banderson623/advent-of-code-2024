from copy import deepcopy
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

EXPLORABLE_SPACES = [".", "E", "S"]
MOVEMENTS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

map = [["." for _ in range(WIDTH)] for _ in range(HEIGHT)]

for y, row in enumerate(input.strip().split("\n")):
    for x, item in enumerate(row.strip()):
        map[y][x] = item

        if item == "E":
            END_LOCATION = (x, y)
        if item == "S":
            START_LOCATION = (x, y)


# Since it's not a maze, a simple path following strategy is fine
def simple_walker(map):
    path = []
    path.append(START_LOCATION)
    at = START_LOCATION

    while at != END_LOCATION:
        for move in MOVEMENTS:
            dx, dy = move
            x, y = at

            if map[dy + y][dx + x] in EXPLORABLE_SPACES and (dx + x, dy + y) not in path:
                path.append((dx + x, dy + y))
                at = (x + dx, y + dy)
                break

    # path.remove(END_LOCATION)
    return path


path = simple_walker(map)
print("baseline pico seconds:", len(path))

total_time = len(path)


def prettyPrint(map):
    for row in map:
        print("".join(row))


# now to see how many cheats, up to size 20, will save us up to
# 100 picoseonds (advance that many steps)
cheats_by_time_saved_counter = {}
CHEAT_DURATION = 20
TIME_SAVED_REQUIREMENT = 100


for index, step in enumerate(path):
    x, y = step
    if index % 100 == 0:
        print(f"working on step {index}")

    for dx in range(-1 * CHEAT_DURATION, CHEAT_DURATION + 1):
        for dy in range(-1 * CHEAT_DURATION, CHEAT_DURATION + 1):

            if dy == 0 and dx == 0:
                continue

            if abs(dx) + abs(dy) > CHEAT_DURATION:
                continue

            if dx + x < 0 or dx + x >= WIDTH or dy + y < 0 or dy + y >= HEIGHT:
                continue

            if map[y][x] == "#":
                continue

            if (dx + x, dy + y) in path:
                cheat_index = path.index((x + dx, y + dy))
                cheat_distance = abs(dx) + abs(dy)

                time_saved = (cheat_index - index) - cheat_distance

                if time_saved >= TIME_SAVED_REQUIREMENT:

                    cheats_by_time_saved_counter[time_saved] = (
                        cheats_by_time_saved_counter[time_saved] + 1
                        if time_saved in cheats_by_time_saved_counter
                        else 1
                    )

times = list(cheats_by_time_saved_counter.keys())
times.sort()
total = 0
for cheat in times:
    total += cheats_by_time_saved_counter[cheat]
    print(f"There are {cheats_by_time_saved_counter[cheat]} cheats that save {cheat} picoseconds")

print(f"total cheats: {total}")
