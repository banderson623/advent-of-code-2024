input = """
AAAA
BBCD
BBCC
EEEC
"""

map = []


# function to display the map
def prettyPrint(map):
    print("+" + "-" * len(map[0]) + "+")
    for y, row in enumerate(map):
        print("|" + "".join(row) + "|")
    print("+" + "-" * len(map[0]) + "+")


plant_counts = {}
plant_locations = {}

# build the map
for [y, row] in enumerate(input.strip().split("\n")):
    row_data = []
    for [x, item] in enumerate(row):
        row_data.append(item)

        if item not in plant_counts:
            plant_counts[item] = 0

        plant_counts[item] += 1

        if item not in plant_locations:
            plant_locations[item] = []

        plant_locations[item].append((x, y))
    map.append(row_data)

prettyPrint(map)

print(plant_counts)

# lets find contiguous plant regions

regions = []

print(plant_locations)

for plant, locations in plant_locations.items():
    print(f"Plant {plant} has {len(locations)} locations")

    this_region = []
    for location in locations:
        x, y = location
        this_region.append(location)
        for next in [(x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)]:
            next_x, next_y = next

            if next in locations and location not in this_region:
                this_region.append(next)

    regions.append((plant, this_region))

print(regions)
