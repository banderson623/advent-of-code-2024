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
#     input = f.read().strip()

map = []

TRAIL = " "
MOVABLE_SPACES = [".", "X", "|", "-", "+", TRAIL]


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
rows = input.split("\n")
for y, row in enumerate(rows):
    map.append([])
    for x, col in enumerate(row):
        map[y].append(col)

bumped_on_up = []
bumped_on_down = []
bumped_on_left = []
bumped_on_right = []

stop_opportunities = []


def take_a_step(starting_map):
    map = starting_map

    height = len(map)
    width = len(map[0])

    guard_on_map = True
    guard_found = False

    global bumped_on_up, bumped_on_left, bumped_on_down, bumped_on_right, stop_opportunities

    for y, row in enumerate(map):
        for x, tile in enumerate(row):
            if not guard_found:
                match tile:
                    case Guard.Up:
                        if y - 1 < 0:
                            map[y][x] = TRAIL
                            guard_on_map = False
                        elif map[y - 1][x] in MOVABLE_SPACES:
                            guard_found = True

                            if y in bumped_on_right:
                                # map[y - 1][x] = "0"

                                stop_opportunities.append((x, y - 1))
                                # return False

                            map[y - 1][x] = Guard.Up
                            map[y][x] = "|"
                        else:
                            bumped_on_up.append(x)
                            map[y][x] = Guard.Right

                    case Guard.Right:
                        if x + 1 >= width:
                            map[y][x] = TRAIL
                            guard_on_map = False
                        elif map[y][x + 1] in MOVABLE_SPACES:
                            guard_found = True

                            if x in bumped_on_down:
                                # map[y][x + 1] = "0"
                                stop_opportunities.append((x + 1, y))
                                # return False

                            map[y][x + 1] = Guard.Right
                            map[y][x] = "-"
                        else:
                            bumped_on_right.append(y)
                            map[y][x] = Guard.Down

                    case Guard.Down:
                        if y + 1 >= height:
                            map[y][x] = TRAIL
                            guard_on_map = False
                        elif map[y + 1][x] in MOVABLE_SPACES:
                            guard_found = True

                            if y in bumped_on_left:
                                # map[y + 1][x] = "0"
                                stop_opportunities.append((x, y + 1))
                                # return False

                            map[y + 1][x] = Guard.Down
                            map[y][x] = "|"
                        else:
                            bumped_on_down.append(y)
                            map[y][x] = Guard.Left

                    case Guard.Left:
                        if x - 1 < 0:
                            map[y][x] = TRAIL
                            guard_on_map = False
                        elif map[y][x - 1] in MOVABLE_SPACES:
                            guard_found = True

                            if x in bumped_on_up:
                                # map[y][x - 1] = "0"
                                stop_opportunities.append((x - 1, y))
                                # return False

                            map[y][x - 1] = Guard.Left
                            map[y][x] = "-"
                        else:
                            bumped_on_left.append(y)
                            map[y][x] = Guard.Up

    return guard_on_map


# prettyPrint(map)
guard_on_map = True

while guard_on_map:

    guard_on_map = take_a_step(map)

    time.sleep(0.05)
    print("\033c")
    prettyPrint(map, stop_opportunities)

    if not guard_on_map:
        print("Guard fell off the map")
        positions_traveled = sum(row.count(TRAIL) for row in map)
        break

print("positions seen:", positions_traveled)
print("bumped_on_up:", bumped_on_up)
print("bumped_on_down:", bumped_on_down)
print("bumped_on_left:", bumped_on_left)
print("bumped_on_right:", bumped_on_right)
print("stop_opportunities:", len(stop_opportunities))


prettyPrint(map, stop_opportunities)

# 942 is too low
