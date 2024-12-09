import re
import os

# sample
input = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"

input_file_path = os.path.join(os.path.dirname(__file__), "input.txt")
with open(input_file_path, "r") as f:
    input = f.read()

# Find all the do() don't() and record when they start
dont_starts = [(m.start(0)) for m in re.finditer(r"don't\(\)", input)]
do_starts = [(m.start(0)) for m in re.finditer(r"do\(\)", input)]

including = True
enabled_input = ""

# Walk through the input character by character
for index, character in enumerate(input):
    if including:
        enabled_input += character
        if index in dont_starts:
            # Just so you can read the output nicely
            enabled_input += "on't()"
            including = False
    else:
        enabled_input += "-"
        if index in do_starts:
            # Just so you can read the output nicely
            enabled_input += "d"
            including = True

# print(enabled_input)

sum = 0
for [left, right] in re.findall(r"mul\((\d+),(\d+)\)", enabled_input):
    product = int(left) * int(right)
    sum += product

print(f"Sum: {sum}")