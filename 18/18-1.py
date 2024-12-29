import heapq

input = """
5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0"""

import os

input_file_path = os.path.join(os.path.dirname(__file__), "input.txt")
with open(input_file_path, "r") as f:
    input = f.read().strip()

max_x = 0
max_y = 0
locations = []

for location in input.strip().split("\n"):
    # print(location.split(","))
    x, y = [int(x) for x in location.split(",")]
    max_x = max(x, max_x)
    max_y = max(y, max_y)
    locations.append((x, y))

# print(locations)

HEIGHT = max_y + 1
WIDTH = max_x + 1
BYTES = 1024
map = [["." for _ in range(WIDTH)] for _ in range(HEIGHT)]

for y in range(HEIGHT):
    for x in range(WIDTH):
        map[y][x] = "#" if (x, y) in locations[:BYTES] else "."


def prettyPrint(map):
    for row in map:
        print("".join(row))


# number of steps and start location (top left), and pathway
queue = [(0, (0, 0), set())]
visited = set()
EXIT_LOCATION = (max_x, max_y)
MOVEMENTS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

prettyPrint(map)

while queue:
    cost, location, path = heapq.heappop(queue)
    path.add(location)

    if location == EXIT_LOCATION:
        print("found exit with steps", cost)
        break

    if location in visited:
        continue

    visited.add(location)

    for move in MOVEMENTS:
        dx, dy = move
        x, y = location

        if HEIGHT > y + dy >= 0 and WIDTH > x + dx >= 0:
            if map[y + dy][x + dx] == "." and (x + dx, y + dy) not in visited:
                heapq.heappush(queue, (cost + 1, (x + dx, y + dy), path.copy()))

print("done exploring")

for loc in path:
    x, y = loc
    map[y][x] = "*"

prettyPrint(map)
