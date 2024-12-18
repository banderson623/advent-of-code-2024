import re

input = """
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400
"""

input = """
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
"""

import os

input_file_path = os.path.join(os.path.dirname(__file__), "input.txt")
with open(input_file_path, "r") as f:
    input = f.read().strip()

machines = input.strip().split("\n\n")


def brute_diophantine(a, b, goal):
    # Nice hint about button presses
    #   "You estimate that each button would need to be pressed no more than
    #    100 times to win a prize...."
    solutions = []
    for x in range(100):
        for y in range(100):
            if a * x + b * y == goal:
                solutions.append((x, y))
    return solutions


prizes = 0
total_tokens = 0
for i, machine in enumerate(machines):
    buttonA, buttonB, prize = machine.split("\n")
    aX, aY = re.findall(r"X\+(\d+), Y\+(\d+)", buttonA)[0]
    bX, bY = re.findall(r"X\+(\d+), Y\+(\d+)", buttonB)[0]
    prizeX, prizeY = re.findall(r"X=(\d+), Y=(\d+)", prize)[0]

    possibleXMoves = brute_diophantine(int(aX), int(bX), int(prizeX))
    possibleYMoves = brute_diophantine(int(aY), int(bY), int(prizeY))
    intersection = set(possibleXMoves).intersection(set(possibleYMoves))

    if not intersection:
        print("No solution found")
        continue

    least_tokens = 1000000000000000000
    prizes += 1
    for a, b in intersection:
        cost = a * 3 + b
        if cost < least_tokens:
            least_tokens = cost
        print(f"Machine {i} --> {cost} tokens - button A: {a} B:{b}")

    total_tokens += least_tokens

print(f"Total prizes: {prizes} for {total_tokens} tokens")

# a = brute_diophantine(94, 22, 8400)
# b = brute_diophantine(34, 67, 5400)

# intersection = set(a).intersection(set(b))
# print("Intersection:", intersection)
