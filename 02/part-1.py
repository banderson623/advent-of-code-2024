import os

sample = """
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""

input_file_path = os.path.join(os.path.dirname(__file__), "input.txt")
with open(input_file_path, "r") as f:
    sample = f.read()

number_of_safe = 0

for line in sample.split("\n"):
    if not line:
        continue

    numbers = [int(num) for num in line.split(" ")]

    safe = True
    direction_i_should_be_going = 0

    for i in range(1, len(numbers)):

        if not safe:
            continue

        diff = numbers[i] - numbers[i - 1]

        this_step_direction = 1 if diff > 0 else -1

        if i == 1:
            direction_i_should_be_going = this_step_direction

        safe = diff != 0 and direction_i_should_be_going == this_step_direction and abs(diff) <= 3

    print(safe, line)
    # number_of_safe += 1 if safe else 0
    if safe:
        number_of_safe += 1

print(f"Number of safe: {number_of_safe}")
