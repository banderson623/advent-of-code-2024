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

# input = """
# 10..9..
# 2...8..
# 3...7..
# 4567654
# ...8..3
# ...9..2
# .....01
# """


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


def prettPrintPath(path, map):
    this_map = []
    for y in range(HEIGHT):
        this_map.append(["."] * WIDTH)

    for location in path:
        x, y = location
        this_map[y][x] = map[y][x]

    prettyPrint(this_map)


def backtracking_path_finding(map, location, current_path, all_paths, trailheads):
    x, y = location

    if location in current_path:
        return all_paths

    current_path.append(location)

    current_elevation = int(map[y][x])

    # I have arrived at a trailhead, yay!
    if location in trailheads:
        all_paths.append(current_path)

    else:
        for next in [(x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)]:
            next_x, next_y = next

            # make sure we aren't off the boundary of the map
            if next_x < 0 or next_x >= WIDTH or next_y < 0 or next_y >= HEIGHT:
                continue

            if map[next_y][next_x] == ".":
                continue

            next_evelvation = int(map[next_y][next_x])

            if next_evelvation == current_elevation - 1:
                # print(f"...going to {next} (from {current_elevation} to {next_evelvation})")
                backtracking_path_finding(map, next, current_path.copy(), all_paths, trailheads)

    # current_path.pop()


# let's walk down from the peaks and see where it goes
for peak in peaks:
    x, y = peak

    all_paths = []
    backtracking_path_finding(map, peak, [], all_paths, trailheads)
    print("------------------------------------------")
    print("Done walking down from peak", peak, "Paths:", len(all_paths))
    # print("Paths:", all_paths)

    for path in all_paths:
        trailhead = path[-1]
        for location in path:
            if location in trailheads:
                scores[trailhead] += 1

        # prettPrintPath(path, map)

print("Scores", scores, sum(scores.values()))
