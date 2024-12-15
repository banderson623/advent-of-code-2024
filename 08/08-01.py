import os

input = """
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
""".strip()

input_file_path = os.path.join(os.path.dirname(__file__), "input.txt")
with open(input_file_path, "r") as f:
    input = f.read().strip()

map = []


# function to display the map
def prettyPrint(map):
    print("+" + "-" * len(map[0]) + "+")
    for y, row in enumerate(map):
        print("|" + "".join(row) + "|")
    print("+" + "-" * len(map[0]) + "+")


# build the map
for [y, row] in enumerate(input.strip().split("\n")):
    row_data = []
    for [x, item] in enumerate(row):
        row_data.append(item)
    map.append(row_data)

prettyPrint(map)

HEIGHT = len(map)
WIDTH = len(map[0])

antennas = []
antenna_frequencies = set()

# Find all antennas
for y in range(HEIGHT):
    for x in range(WIDTH):
        val = map[y][x]
        is_antenna = val != "."
        if is_antenna:
            antenna_frequencies.add(val)
            antennas.append((x, y, val))

print("Antenna frequencies", antenna_frequencies)

antinodes = set()

for frequency in antenna_frequencies:
    same_frequency_antennas = [antenna for antenna in antennas if antenna[2] == frequency]
    for antenna in same_frequency_antennas:
        x, y, val = antenna
        other_antennas = [ant for ant in same_frequency_antennas if ant != antenna]
        for other_antenna in other_antennas:
            x2, y2, val2 = other_antenna
            dx = x - x2
            dy = y - y2

            # we can add this as long as its within the bounds of the map
            if x + dx in range(0, WIDTH) and y + dy in range(0, HEIGHT):
                antinodes.add((x + dx, y + dy))

for antinode in antinodes:
    x, y = antinode
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        map[y][x] = "*"

prettyPrint(map)
print(f"Unique antinode locations: {len(antinodes)}")
