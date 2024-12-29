import functools

input = """
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
"""

import os

input_file_path = os.path.join(os.path.dirname(__file__), "input.txt")
with open(input_file_path, "r") as f:
    input = f.read().strip()


towels_list, patterns_list = input.strip().split("\n\n")
towels = towels_list.split(", ")


@functools.lru_cache(maxsize=None)
def count_possible_towel_combos(pattern_fragment):
    if len(pattern_fragment) == 0:
        return 1

    remaining_to_check = []

    for towel in towels:
        if towel == pattern_fragment[: len(towel)]:
            remaining_to_check.append(count_possible_towel_combos(pattern_fragment[len(towel) :]))

    if len(remaining_to_check):
        return sum(remaining_to_check)

    # There is still pattern fragment remaining and it's not been solved
    return 0


total_combos = 0
for pattern in patterns_list.split("\n"):
    possible_combos = count_possible_towel_combos(pattern)
    total_combos += possible_combos

    print("possible towel combos", possible_combos, pattern)


print(f"total combos: {total_combos}")
