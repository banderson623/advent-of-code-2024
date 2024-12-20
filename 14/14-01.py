import re
from time import sleep

WIDTH = 101
HEIGHT = 103

input = "p=2,4 v=2,-3"

input = """
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
"""

import os

input_file_path = os.path.join(os.path.dirname(__file__), "input.txt")
with open(input_file_path, "r") as f:
    input = f.read().strip()

robots = []
for line in input.strip().split("\n"):
    x, y, dx, dy = map(int, re.findall(r"([0-9]+),([0-9]+).*=([-0-9]+),([-0-9]+)", line)[0])
    print(line, "->", x, y, dx, dy)
    robots.append({"p": (x, y), "v": (dx, dy)})


def prettyPrint(robots, with_quadrants=True):
    map = [["." for _ in range(WIDTH)] for _ in range(HEIGHT)]

    for robot in robots:
        x, y = robot["p"]
        map[y][x] = str(int(map[y][x]) + 1) if map[y][x] != "." else "1"

    if with_quadrants:
        half_vertical = HEIGHT // 2
        half_horizontal = WIDTH // 2

        for y in range(HEIGHT):
            map[y][half_horizontal] = "|"

        map[half_vertical] = ["~" for _ in range(WIDTH)]
        map[half_vertical][half_horizontal] = "+"

    print("+" + "-" * len(map[0]) + "+")
    for row in map:
        print("|" + "".join(row) + "|")
    print("+" + "-" * len(map[0]) + "+")


prettyPrint(robots, with_quadrants=False)

for second in range(100):
    for robot in robots:
        x, y = robot["p"]
        next_x = (x + robot["v"][0]) % WIDTH
        next_y = (y + robot["v"][1]) % HEIGHT
        robot["p"] = (next_x, next_y)

quadrantsCount = [0, 0, 0, 0]

for robot in robots:
    x, y = robot["p"]

    if x < WIDTH // 2:
        if y < HEIGHT // 2:
            quadrantsCount[0] += 1
        elif y > HEIGHT // 2:
            quadrantsCount[1] += 1
    elif x > WIDTH // 2:
        if y < HEIGHT // 2:
            quadrantsCount[2] += 1
        elif y > HEIGHT // 2:
            quadrantsCount[3] += 1


prettyPrint(robots)
print(quadrantsCount)
print("Product of quadrants", quadrantsCount[0] * quadrantsCount[1] * quadrantsCount[2] * quadrantsCount[3])
