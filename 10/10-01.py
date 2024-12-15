input = """
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""

input = """
10..9..
2...8..
3...7..
4567654
...8..3
...9..2
.....01
"""


trailheads = []
peaks = []
scores = {}
map = []

for [y, row] in enumerate(input.strip().split("\n")):
    row_data = []
    for [x, item] in enumerate(row):
        if item == "0":
            trailheads.append((x, y))
            scores[(x, y)] = 0
        elif item == "9":
            peaks.append((x, y))
        row_data.append(item)
    map.append(row_data)

HEIGHT = len(map)
WIDTH = len(map[0])


def prettyPrint(map):
    print("+" + "-" * len(map[0]) + "+")
    for y, row in enumerate(map):
        print("|" + "".join(row) + "|")
    print("+" + "-" * len(map[0]) + "+")


prettyPrint(map)
print("Trailheads", trailheads)
print("Peaks", peaks)

# let's walk down from the peaks and see where it goes

for peak in peaks:
    x, y = peak

    # python is silly the end range is not inclusive

    for next in range(8, -1, -1):
        # print("...at", x, y, "looking for", next)

        # check up
        if map[max(0, y - 1)][x] == str(next):
            y -= 1

        # check down
        elif map[min(y + 1, HEIGHT - 1)][x] == str(next):
            y += 1

        # check right
        elif map[y][min(x + 1, WIDTH - 1)] == str(next):
            x += 1

        # check left
        elif map[y][max(0, x - 1)] == str(next):
            x -= 1
        else:
            print("Dead End, could not find", next, "neighboring: ", x, y)
            break

        if next == 0:
            print("arrived at trailhead", x, y)
            scores[(x, y)] += 1
            break


print("Scores", scores, sum(scores.values()))
