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
def can_build_pattern(pattern_fragment):
    if len(pattern_fragment) == 0:
        return True

    remaining_to_check = []

    for towel in towels:
        if towel == pattern_fragment[: len(towel)]:
            remaining_to_check.append(can_build_pattern(pattern_fragment[len(towel) :]))

    if True in remaining_to_check:
        return True

    # There is still pattern fragment remaining and it's not been solved
    return False


impossible_counter = 0
possible_counter = 0
for pattern in patterns_list.split("\n"):
    print("working on pattern:", pattern)

    if can_build_pattern(pattern):
        possible_counter += 1
    else:
        impossible_counter += 1

print("Impossible patterns", impossible_counter)
print("possible patterns", possible_counter)


# 220 is too low
