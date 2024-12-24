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

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# """

# input = """
# #####
# #...#
# #.O.#
# #@O.#
# #...#
# #####

# >v>^
# """

# input = """
# #####
# #O..#
# #...#
# #O..#
# #.@.#
# #####

# <^^^
# """

# input = """
# #####
# #...#
# #@O.#
# #..O#
# #...#
# #####

# >>^>v
# """

# input = """
# #######
# #...#.#
# #.....#
# #..OO@#
# #..O..#
# #.....#
# #######

# <vv<<^^<<^^
# """

import os

input_file_path = os.path.join(os.path.dirname(__file__), "input.txt")
with open(input_file_path, "r") as f:
    input = f.read().strip()

warehouse, moves = [x.strip() for x in input.strip().split("\n\n")]

# Super size the map
warehouse = warehouse.replace("#", "##")
warehouse = warehouse.replace("O", "[]")
warehouse = warehouse.replace(".", "..")
warehouse = warehouse.replace("@", "@.")

# Make all the moves just one long list
moves = "".join(moves.split("\n"))

HEIGHT = len(warehouse.split("\n"))
WIDTH = len(warehouse.split("\n")[0])
ROBOT_SYMBOL = "@"
EMPTY_SYMBOL = "."
BOX_SYMBOLS = ["[", "]"]
WALL_SYMBOL = "#"
LEFT_SIDE_OF_BOX = BOX_SYMBOLS[0]
RIGHT_SIDE_OF_BOX = BOX_SYMBOLS[1]


print("Width:", WIDTH, "Height:", HEIGHT, BOX_SYMBOLS)

map = [["." for _ in range(WIDTH)] for _ in range(HEIGHT)]

robot_location = (0, 0)

# build map
for y, row in enumerate(warehouse.split("\n")):
    for x, item in enumerate(row):
        map[y][x] = item
        if item == ROBOT_SYMBOL:
            robot_location = (x, y)


def prettyPrint(map):
    for row in map:
        print("".join(row))


MOVE_MAP = {"v": (0, 1), "^": (0, -1), ">": (1, 0), "<": (-1, 0)}

prettyPrint(map)


def can_compact(x, y, direction, map):
    # print(f"can_compact ({x},{y}) in {direction} ? piece: {map[y][x]}")
    (dx, dy) = MOVE_MAP[direction]

    # Looking for an empty space or wall
    check_x = x + dx
    check_y = y + dy

    if map[check_y][check_x] == EMPTY_SYMBOL:
        return True
    if map[check_y][check_x] == WALL_SYMBOL:
        return False

    # This is way more complex, it needs to support looking up/down
    # to support...  (this lil guy is pushing up)
    #  ##############
    #  ##......##..##
    #  ##..........##
    #  ##...[][]...##
    #  ##....[]....##
    #  ##.....@....##
    #  ##############

    # horizontal move, easy

    # if moving vertically
    if dy != 0 and map[check_y][check_x] in BOX_SYMBOLS:
        if map[check_y][check_x] == BOX_SYMBOLS[0]:
            return can_compact(check_x, check_y, direction, map) and can_compact(check_x + 1, check_y, direction, map)
        else:
            return can_compact(check_x, check_y, direction, map) and can_compact(check_x - 1, check_y, direction, map)

    else:
        return can_compact(check_x, check_y, direction, map)


def push_boxes(x, y, direction, map):

    if x < 0 or y < 0:
        return

    piece_being_pushed = map[y][x]

    if piece_being_pushed not in BOX_SYMBOLS:
        return

    (dx, dy) = MOVE_MAP[direction]

    is_horizontal_move = dy == 0
    is_vertical_move = dy != 0

    # Where the box will be pushed...
    pushed_x = x + (dx * 2)  # *2 because it's supersized
    pushed_y = y + dy

    # Push additional boxes (first, recursively)
    if map[pushed_y][pushed_x] in BOX_SYMBOLS:
        push_boxes(pushed_x, pushed_y, direction, map)

    # account for the case where the box's side is impacting
    # another box...
    #
    # Pushing "up"
    #    +------------+
    #    |.......##...|
    #    |............|
    #    |....[][]....|
    #    |.....[].....|
    #    |......@.....|
    #    +------------+
    # on a vertical move, account for the left side of the box being pushed
    if map[y][x] == RIGHT_SIDE_OF_BOX and is_vertical_move:
        push_boxes(pushed_x - 1, pushed_y, direction, map)

    if map[y][x] == LEFT_SIDE_OF_BOX and is_vertical_move:
        push_boxes(pushed_x + 1, pushed_y, direction, map)

    if is_horizontal_move:
        for x_adder, symbol in enumerate(BOX_SYMBOLS):

            # if moving right x has already had +1 added to it
            if direction == ">":
                x_adder -= 1

            map[pushed_y][pushed_x + x_adder] = symbol

    else:  # vertical_move
        if map[y][x] == LEFT_SIDE_OF_BOX:
            map[pushed_y][pushed_x] = BOX_SYMBOLS[0]
            map[pushed_y][pushed_x + 1] = BOX_SYMBOLS[1]
            map[y][x + 1] = EMPTY_SYMBOL
        elif map[y][x] == RIGHT_SIDE_OF_BOX:
            map[pushed_y][pushed_x - 1] = BOX_SYMBOLS[0]
            map[pushed_y][pushed_x] = BOX_SYMBOLS[1]
            map[y][x - 1] = EMPTY_SYMBOL
        map[y][x] = EMPTY_SYMBOL


def can_move(x, y, direction, map):
    x, y = robot_location
    (dx, dy) = MOVE_MAP[direction]
    future_x, future_y = x + dx, y + dy
    if map[future_y][future_x] == EMPTY_SYMBOL:
        return True
    elif map[future_y][future_x] == WALL_SYMBOL:
        return False
    elif map[future_y][future_x] in BOX_SYMBOLS:
        return can_compact(x, y, direction, map)

    else:
        return False


for desired_move in moves:
    (dx, dy) = MOVE_MAP[desired_move]
    (x, y) = robot_location

    if can_move(x, y, desired_move, map):
        if map[y + dy][x + dx] in BOX_SYMBOLS:
            push_boxes(x + dx, y + dy, desired_move, map)

        map[y][x] = EMPTY_SYMBOL
        map[y + dy][x + dx] = ROBOT_SYMBOL
        robot_location = (x + dx, y + dy)

    # prettyPrint(map)
    # sleep(0.5)
    # sleep(0.1)

prettyPrint(map)

# Calculate GPS sum
gps_sum = 0
for y, row in enumerate(map):
    for x, item in enumerate(row):
        # just count the left side (closest to top right)
        if item == LEFT_SIDE_OF_BOX:
            gps_sum += y * 100 + x

print(f"gps sum: {gps_sum}")
