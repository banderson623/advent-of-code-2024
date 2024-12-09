import re
import os


contents = """
3   4
4   3
2   5
1   3
3   9
3   3
"""

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

# print(firsts)
# print(lasts)

sum_by_using_frequency = 0

for item in firsts:
    # this was fun, i didn't know about "count" method
    sum_by_using_frequency += item * lasts.count(item)

print(f"Part 2 - Sum: {sum_by_using_frequency}")
