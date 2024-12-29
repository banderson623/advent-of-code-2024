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

# import os

# input_file_path = os.path.join(os.path.dirname(__file__), "input.txt")
# with open(input_file_path, "r") as f:
#     input = f.read().strip()


towels_list, patterns_list = input.strip().split("\n\n")
towels = towels_list.split(", ")

# largest towel first
towels.sort(key=len, reverse=True)

another = towels.copy()
another.sort()
print(f" alph sorted towels: {another}")


def towels_for_pattern(pattern_fragment):
    if len(pattern_fragment) == 0:
        return []

    for towel in towels:
        if towel == pattern_fragment[: len(towel)]:
            unmatched_pattern = pattern_fragment[len(towel) :]
            return [towel] + towels_for_pattern(unmatched_pattern)

    # There is still pattern fragment remaining and it's not been solved
    print(f"so close, but {pattern_fragment} has no match")
    return [False]


impossible_counter = 0
possible_counter = 0
for pattern in patterns_list.split("\n"):
    # print("working on pattern:", pattern)
    required_towels = towels_for_pattern(pattern)

    if False in required_towels:
        impossible_counter += 1
    else:
        possible_counter += 1


print("Impossible patterns", impossible_counter)
print("possible patterns", possible_counter)


# 220 is too low
