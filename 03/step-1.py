import re
import os

input = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"

input_file_path = os.path.join(os.path.dirname(__file__), "input.txt")
with open(input_file_path, "r") as f:
    input = f.read()

sum = 0
for [left, right] in re.findall(r"mul\((\d+),(\d+)\)", input):
    product = int(left) * int(right)
    sum += product

print(f"Sum: {sum}")
