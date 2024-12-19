import re
from sympy import symbols, Eq, solve

# input = """
# Button A: X+94, Y+34
# Button B: X+22, Y+67
# Prize: X=10000000008400, Y=10000000005400
# """

input = """
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=10000000008400, Y=10000000005400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=10000000012748, Y=10000000012176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=10000000007870, Y=10000000006450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=10000000018641, Y=10000000010279
"""

import os

input_file_path = os.path.join(os.path.dirname(__file__), "input.txt")
with open(input_file_path, "r") as f:
    input = f.read().strip()

machines = input.strip().split("\n\n")


def liner_solver(aX, aY, goalA, bX, bY, goalB):
    # Define symbolic variables
    a, b = symbols("a b", integer=True)

    # Define the equations

    # print(f"1 = a * aX({aX}) + b * aY({aY}), {goalA}")
    # print(f"1 = a * bX({bX}) + b * bY({bY}), {goalB}")

    eq1 = Eq(a * aX + b * bX, goalA)
    eq2 = Eq(a * aY + b * bY, goalB)

    # Solve the system of equations
    solutions = solve([eq1, eq2], (a, b))
    # print(f"Solution", solutions)
    return solutions


prizes = 0
total_tokens = 0
goal_bump = 10000000000000

for i, machine in enumerate(machines):
    buttonA, buttonB, prize = machine.split("\n")
    aX, aY = re.findall(r"X\+(\d+), Y\+(\d+)", buttonA)[0]
    bX, bY = re.findall(r"X\+(\d+), Y\+(\d+)", buttonB)[0]
    prizeX, prizeY = re.findall(r"X=(\d+), Y=(\d+)", prize)[0]

    # print(f"Machine {i} - Button A: {aX}, {aY} - Button B: {bX}, {bY} - Prize: {prizeX}, {prizeY}")
    solutions = liner_solver(int(aX), int(aY), int(prizeX) + goal_bump, int(bX), int(bY), int(prizeY) + goal_bump)

    if not solutions:
        # print("No solution found")
        continue

    least_tokens = 1000000000000000000
    prizes += 1

    a, b = solutions.values()
    # print(value)
    cost = a * 3 + b
    if cost < least_tokens:
        least_tokens = cost
    print(f"Machine {i} --> {cost} tokens - button A: {a} B:{b}")

    total_tokens += least_tokens

print(f"Total prizes: {prizes} for {total_tokens} tokens")
