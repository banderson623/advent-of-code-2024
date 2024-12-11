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

# input_file_path = os.path.join(os.path.dirname(__file__), "input.txt")
# with open(input_file_path, "r") as f:
#     input = f.read()

map = []

MOVABLE_SPACES = [".", "X"]


class Guard:
    Up = "^"
    Right = ">"
    Down = "v"
    Left = "<"


def prettyPrint(map):
    print("+" + "-" * len(map[0]) + "+")
    for row in map:
        print("|" + "".join(row) + "|")
    print("+" + "-" * len(map[0]) + "+")


# Lets put them all into a 2D array
rows = input.split("\n")
for y, row in enumerate(rows):
    map.append([])
    for x, col in enumerate(row):
        map[y].append(col)


def take_a_step(starting_map):
    map = starting_map

    height = len(map)
    width = len(map[0])

    guard_on_map = True
    guard_found = False

    for y, row in enumerate(map):
        if guard_found:
            break
        for x, tile in enumerate(row):
            if guard_found:
                break
            match tile:
                case Guard.Up:
                    if y - 1 < 0:
                        map[y][x] = "X"
                        guard_on_map = False
                    elif map[y - 1][x] in MOVABLE_SPACES:
                        guard_found = True
                        map[y - 1][x] = Guard.Up
                        map[y][x] = "X"
                    else:
                        map[y][x] = Guard.Right

                case Guard.Right:
                    if x + 1 >= width:
                        map[y][x] = "X"
                        guard_on_map = False
                    elif map[y][x + 1] in MOVABLE_SPACES:
                        guard_found = True
                        map[y][x + 1] = Guard.Right
                        map[y][x] = "X"
                    else:
                        map[y][x] = Guard.Down

                case Guard.Down:
                    if y + 1 >= height:
                        map[y][x] = "X"
                        guard_on_map = False
                    elif map[y + 1][x] in MOVABLE_SPACES:
                        guard_found = True
                        map[y + 1][x] = Guard.Down
                        map[y][x] = "X"
                    else:
                        map[y][x] = Guard.Left

                case Guard.Left:
                    if x - 1 < 0:
                        map[y][x] = "X"
                        guard_on_map = False
                    elif map[y][x - 1] in MOVABLE_SPACES:
                        guard_found = True
                        map[y][x - 1] = Guard.Left
                        map[y][x] = "X"
                    else:
                        map[y][x] = Guard.Up

    return guard_on_map


# prettyPrint(map)
guard_on_map = True

while guard_on_map:

    time.sleep(0.1)

    # clear the screen
    print("\033c")

    guard_on_map = take_a_step(map)
    prettyPrint(map)

    if not guard_on_map:
        print("Guard fell off the map")
        positions_traveled = sum(row.count("X") for row in map)
        break

print("positions seen:", positions_traveled)
