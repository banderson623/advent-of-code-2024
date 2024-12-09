import os

sample = """
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""


def is_report_safe(levels):
    direction_of_travel = None

    for i in range(1, len(levels)):
        last_level = levels[i - 1]
        this_level = levels[i]

        step_size = this_level - last_level

        if step_size == 0:
            # Unsafe, level change is required
            return False

        if abs(step_size) > 3:
            # Unsafe, Too big of a step
            return False

        this_step_direction_of_travel = "up" if step_size > 0 else "down"

        if i == 1:
            # set the direction on the first transition
            direction_of_travel = this_step_direction_of_travel

        if direction_of_travel != this_step_direction_of_travel:
            # unsafe, it switch from up to down, or down to up
            return False

    return True


# lets do a terrible brute force hack, try removing
# one level at a time, to see if it's ever safe.
def try_to_remove_any_step_to_see_if_its_safe(levels):
    for i in range(0, len(levels)):
        modified_levels = levels.copy()
        modified_levels.pop(i)
        safe = is_report_safe(modified_levels)
        if safe:
            # the moment it's safe, we can return
            return True

    # hey if you got here and haven't returned safe above, you are unsafe
    return False


# =====================================================================
#                            Main Code
# =====================================================================

# Load the input
input_file_path = os.path.join(os.path.dirname(__file__), "input.txt")
with open(input_file_path, "r") as f:
    sample = f.read()

# initialize number of safe to 0
number_of_safe = 0

# walk through each row of the input
for line in sample.split("\n"):
    if not line:
        continue

    # convert values to integer
    levels = [int(num) for num in line.split(" ")]

    # check if this is safe
    safe = is_report_safe(levels)

    # if not, lets remove any step to see if it's safe
    if not safe:
        safe = try_to_remove_any_step_to_see_if_its_safe(levels)

    if safe:
        number_of_safe += 1

print(f"Number of safe: {number_of_safe}")
