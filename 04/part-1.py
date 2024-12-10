import os

input = """
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""

input_file_path = os.path.join(os.path.dirname(__file__), "input.txt")
with open(input_file_path, "r") as f:
    input = f.read()

board = [list(row) for row in input.strip().split("\n")]
MAX_X = len(board[0])
MAX_Y = len(board)


patterns = {
    "down": [
        ["X"],
        ["M"],
        ["A"],
        ["S"],
    ],
    "up": [
        ["S"],
        ["A"],
        ["M"],
        ["X"],
    ],
    "right": [["X", "M", "A", "S"]],
    "left": [["S", "A", "M", "X"]],
    "up-left": [
        ["S", None, None, None],
        [None, "A", None, None],
        [None, None, "M", None],
        [None, None, None, "X"],
    ],
    "up-right": [
        [None, None, None, "S"],
        [None, None, "A", None],
        [None, "M", None, None],
        ["X", None, None, None],
    ],
    "down-left": [
        [None, None, None, "X"],
        [None, None, "M", None],
        [None, "A", None, None],
        ["S", None, None, None],
    ],
    "down-right": [
        ["X", None, None, None],
        [None, "M", None, None],
        [None, None, "A", None],
        [None, None, None, "S"],
    ],
}


def find_matrix(board, board_x, board_y, lookup_matrix):
    for y, row in enumerate(lookup_matrix):
        for x, letter in enumerate(row):
            if letter is None:
                continue
            if board_y + y >= MAX_Y:
                return False
            if board_x + x >= MAX_X:
                return False
            if letter != board[board_y + y][board_x + x]:
                return False
    return True


total_finds = 0
for y, row in enumerate(board):
    for x, letter in enumerate(row):
        # print(x, y, letter)

        for pattern_name in patterns.keys():
            pattern = patterns[pattern_name]
            if find_matrix(board, x, y, pattern):
                total_finds += 1
                print(f"Found XMAS {pattern_name} at", x, y)

print("total finds", total_finds)
