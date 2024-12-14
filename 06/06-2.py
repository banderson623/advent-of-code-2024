import copy
import time
import os

input = """
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
""".strip()

input_file_path = os.path.join(os.path.dirname(__file__), "input.txt")
with open(input_file_path, "r") as f:
    input = f.read()

map = []

MOVABLE_SPACES = [".", "X"]


class Guard:
    Up = "^"
    Right = ">"
    Down = "v"
    Left = "<"


def prettyPrint(map, stop_opportunities=[]):
    print("+" + "-" * len(map[0]) + "+")
    for y, row in enumerate(map):
        row = [col if (x, y) not in stop_opportunities else "0" for x, col in enumerate(row)]
        print("|" + "".join(row) + "|")
    print("+" + "-" * len(map[0]) + "+")


# Lets put them all into a 2D array
rows = input.strip().split("\n")
for y, row in enumerate(rows):
    map.append([])
    for x, col in enumerate(row):
        map[y].append(col)


def find_guard(map):
    look_ups_to_find_guard = 0
    for y, row in enumerate(map):
        for x, tile in enumerate(row):
            look_ups_to_find_guard += 1
            if tile in [Guard.Up, Guard.Right, Guard.Down, Guard.Left]:
                # print(f"I found the guard, it took {look_ups_to_find_guard} steps")
                return x, y

    return None


def take_a_fast_step(map, prior_guard_location=None):
    guard_on_map = True
    guard_location = None

    height = len(map)
    width = len(map[0])

    if prior_guard_location:
        # just snag the first to elements, x and y, we don't need direction
        x, y = prior_guard_location[:2]
    else:
        x, y = find_guard(map)

    tile = map[y][x]
    try:
        match tile:
            case Guard.Up:
                if y - 1 < 0:
                    map[y][x] = "X"
                    guard_on_map = False
                elif map[y - 1][x] in MOVABLE_SPACES:
                    map[y - 1][x] = Guard.Up
                    guard_location = (x, y - 1, Guard.Up)
                    map[y][x] = "X"
                else:
                    map[y][x] = Guard.Right
                    guard_location = (x, y, Guard.Right)

            case Guard.Right:
                if x + 1 >= width:
                    map[y][x] = "X"
                    guard_on_map = False
                elif map[y][x + 1] in MOVABLE_SPACES:
                    map[y][x + 1] = Guard.Right
                    guard_location = (x + 1, y, Guard.Right)
                    map[y][x] = "X"
                else:
                    map[y][x] = Guard.Down
                    guard_location = (x, y, Guard.Down)

            case Guard.Down:
                if y + 1 >= height:
                    map[y][x] = "X"
                    guard_on_map = False
                elif map[y + 1][x] in MOVABLE_SPACES:
                    map[y + 1][x] = Guard.Down
                    guard_location = (x, y + 1, Guard.Down)
                    map[y][x] = "X"
                else:
                    guard_location = (x, y, Guard.Left)
                    map[y][x] = Guard.Left

            case Guard.Left:
                if x - 1 < 0:
                    map[y][x] = "X"
                    guard_on_map = False
                elif map[y][x - 1] in MOVABLE_SPACES:
                    map[y][x - 1] = Guard.Left
                    guard_location = (x - 1, y, Guard.Left)
                    map[y][x] = "X"
                else:
                    map[y][x] = Guard.Up
                    guard_location = (x, y, Guard.Up)

    except Exception as e:
        print(f"things got weird with", y, x)
        print(f"print height {height} and width {width}")
        prettyPrint(map)
        raise e

    return guard_on_map, guard_location


def take_a_step(map):
    height = len(map)
    width = len(map[0])

    guard_on_map = True
    guard_location = None

    for y, row in enumerate(map):
        if guard_location:
            break
        for x, tile in enumerate(row):
            if guard_location:
                break
            match tile:
                case Guard.Up:
                    guard_location = (x, y, Guard.Up)
                    if y - 1 < 0:
                        map[y][x] = "X"
                        guard_on_map = False
                    elif map[y - 1][x] in MOVABLE_SPACES:
                        map[y - 1][x] = Guard.Up
                        map[y][x] = "X"
                    else:
                        map[y][x] = Guard.Right

                case Guard.Right:
                    guard_location = (x, y, Guard.Right)
                    if x + 1 >= width:
                        map[y][x] = "X"
                        guard_on_map = False
                    elif map[y][x + 1] in MOVABLE_SPACES:
                        map[y][x + 1] = Guard.Right
                        map[y][x] = "X"
                    else:
                        map[y][x] = Guard.Down

                case Guard.Down:
                    guard_location = (x, y, Guard.Down)
                    if y + 1 >= height:
                        map[y][x] = "X"
                        guard_on_map = False
                    elif map[y + 1][x] in MOVABLE_SPACES:
                        map[y + 1][x] = Guard.Down
                        map[y][x] = "X"
                    else:
                        map[y][x] = Guard.Left

                case Guard.Left:
                    guard_location = (x, y, Guard.Left)
                    if x - 1 < 0:
                        map[y][x] = "X"
                        guard_on_map = False
                    elif map[y][x - 1] in MOVABLE_SPACES:
                        map[y][x - 1] = Guard.Left
                        map[y][x] = "X"
                    else:
                        map[y][x] = Guard.Up

    return guard_on_map, guard_location


def is_in_a_loop(map, obstruction_placement):
    all_locations = {}

    map_with_obstruction = copy.deepcopy(map)
    x, y = obstruction_placement
    map_with_obstruction[y][x] = "#"
    location = None

    while True:
        guard_on_map, location = take_a_fast_step(map_with_obstruction, location)

        if location and location in all_locations:
            return True

        if location:
            all_locations[location] = True

        if not guard_on_map:
            return False


height = len(map)
width = len(map[0])

obstructions = []

for y in range(height):
    print(f"row: {y}")
    for x in range(width):
        if map[y][x] == ".":
            if is_in_a_loop(map, (x, y)):
                obstructions.append((x, y))

print(obstructions)
print(f"obstructions for loops possible: {obstructions}")
