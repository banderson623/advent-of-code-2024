from time import sleep


input = """
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
"""

# input = """
# ###########
# #@..O..O.O#
# ###########

# >>>>>>>>
# """

import os

input_file_path = os.path.join(os.path.dirname(__file__), "input.txt")
with open(input_file_path, "r") as f:
    input = f.read().strip()

warehouse, moves = [x.strip() for x in input.strip().split("\n\n")]

# Make all the moves just one long list
moves = "".join(moves.split("\n"))

HEIGHT = len(warehouse.split("\n"))
WIDTH = len(warehouse.split("\n")[0])
ROBOT_SYMBOL = "@"
EMPTY_SYMBOL = "."
BOX_SYMBOL = "O"
WALL_SYMBOL = "#"


print("Width:", WIDTH, "Height:", HEIGHT)

map = [["." for _ in range(WIDTH)] for _ in range(HEIGHT)]

robot_location = (0, 0)

for y, row in enumerate(warehouse.split("\n")):
    for x, item in enumerate(row):
        map[y][x] = item
        if item == ROBOT_SYMBOL:
            robot_location = (x, y)


def prettyPrint(map):
    for row in map:
        print("".join(row))


MOVE_MAP = {"v": (0, 1), "^": (0, -1), ">": (1, 0), "<": (-1, 0)}


def can_compact(x, y, direction, map):
    (dx, dy) = MOVE_MAP[direction]

    # Looking for an empty space or wall
    check_x = x + dx
    check_y = y + dy

    if map[check_y][check_x] == EMPTY_SYMBOL:
        return True
    if map[check_y][check_x] == WALL_SYMBOL:
        return False

    return can_compact(check_x, check_y, direction, map)


def push_boxes(x, y, move, map):
    (dx, dy) = MOVE_MAP[move]

    # Where the box will be pushed...
    pushed_x = x + dx
    pushed_y = y + dy

    if map[pushed_y][pushed_x] == BOX_SYMBOL:
        push_boxes(pushed_x, pushed_y, move, map)

    map[pushed_y][pushed_x] = BOX_SYMBOL
    map[y][x] = EMPTY_SYMBOL


def can_move(x, y, move, map):
    x, y = robot_location
    (dx, dy) = MOVE_MAP[move]
    future_x, future_y = x + dx, y + dy
    if map[future_y][future_x] == EMPTY_SYMBOL:
        return True
    elif map[future_y][future_x] == WALL_SYMBOL:
        return False
    elif map[future_y][future_x] == BOX_SYMBOL:
        can = can_compact(x, y, move, map)
        return can
    else:
        return False


for desired_move in moves:

    (dx, dy) = MOVE_MAP[desired_move]
    (x, y) = robot_location

    if can_move(x, y, desired_move, map):
        if map[y + dy][x + dx] == BOX_SYMBOL:
            push_boxes(x + dx, y + dy, desired_move, map)

        map[y][x] = EMPTY_SYMBOL
        map[y + dy][x + dx] = ROBOT_SYMBOL
        robot_location = (x + dx, y + dy)

    # prettyPrint(map)
    # sleep(0.1)

prettyPrint(map)

# Calculate GPS sum
gps_sum = 0
for y, row in enumerate(map):
    for x, item in enumerate(row):
        if item == BOX_SYMBOL:
            gps_sum += y * 100 + x

print(f"gps sum: {gps_sum}")
