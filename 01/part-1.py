import re
import os

contents = """
3   4
4   3
2   5
1   3
3   9
3   3
""".strip()

input_file_path = os.path.join(os.path.dirname(__file__), "input.txt")
with open(input_file_path, "r") as f:
    contents = f.read()

lines = contents.split("\n")

firsts = []
lasts = []

# pivot the inputs
for line in lines:
    if not line:
        continue

    first, last = re.split(r"\s+", line)

    firsts.append(int(first))
    lasts.append(int(last))

# order ascending
firsts.sort()
lasts.sort()

# Part 1
sum_of_diffs = 0
for index in range(len(firsts)):
    diff = abs(firsts[index] - lasts[index])
    sum_of_diffs += diff

print(f"Part 1 - All the diffs: {sum_of_diffs}")
