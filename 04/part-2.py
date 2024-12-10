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
    "all-down": [
        ["M", None, "M"],
        [None, "A", None],
        ["S", None, "S"],
    ],
    "all-up": [
        ["S", None, "S"],
        [None, "A", None],
        ["M", None, "M"],
    ],
    "first-down": [
        ["M", None, "S"],
        [None, "A", None],
        ["M", None, "S"],
    ],
    "last-down": [
        ["S", None, "M"],
        [None, "A", None],
        ["S", None, "M"],
    ],
}


def find_matrix(board, board_x, board_y, lookup_matrix):
    for y, row in enumerate(lookup_matrix):
        for x, letter in enumerate(row):
            if letter is None:  # we can ignore Nones
                continue
            if board_y + y >= MAX_Y:  # fail if at an edge
                return False
            if board_x + x >= MAX_X:  # fail if at an edge
                return False
            if letter != board[board_y + y][board_x + x]:
                return False
    return True


total_finds = 0
for y, row in enumerate(board):
    for x, letter in enumerate(row):

        for pattern_name in patterns.keys():
            pattern = patterns[pattern_name]
            if find_matrix(board, x, y, pattern):
                total_finds += 1
                print(f"Found XMAS {pattern_name} at", x, y)

print("total finds", total_finds)
