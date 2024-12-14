import os
from itertools import product

input = """
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
""".strip()


input_file_path = os.path.join(os.path.dirname(__file__), "input.txt")
with open(input_file_path, "r") as f:
    input = f.read().strip()

POSSIBLE_OPERATORS = {"+": lambda a, b: a + b, "*": lambda a, b: a * b}


# recursive fun....
# this is going left to right, without any worry about precident
def evaluate(components, permutation):
    right = components[-1]
    op = POSSIBLE_OPERATORS[permutation[-1]]

    if len(components[:-1]) > 1:
        return op(evaluate(components[:-1], permutation[:-1]), right)
    else:
        return op(components[0], right)


sum = 0

for line in input.strip().split("\n"):
    solved = False
    result_string, components_string = line.split(":")
    components = [(int(x)) for x in components_string.strip().split(" ")]
    result = int(result_string)
    number_of_slots = len(components) - 1
    # print(result, components, number_of_slots)

    permutations = product(POSSIBLE_OPERATORS, repeat=number_of_slots)

    for permutation in permutations:
        value = evaluate(components, permutation)
        if result == value:
            # print(value, "*****")
            sum += value
            break

print(f"Sum is {sum}")
