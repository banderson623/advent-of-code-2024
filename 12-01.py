input = """
AAAA
BBCD
BBCC
EEEC
"""

input = """OOOOO
OXOXO
OOOOO
OXOXO
OOOOO"""

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

    total_plants_of_type = len(locations)
    found_plants = []

    while len(found_plants) < total_plants_of_type:

        this_region = []

        # The first locations not in found_plants
        location = [x for x in locations if x not in found_plants][0]

        # remember I found this plant
        this_region.append(location)
        found_plants.append(location)

        x, y = location

        # let's look for a cotinuous plant region
        for next in [(x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)]:
            next_x, next_y = next

            if next in locations and next not in this_region:

                found_plants.append(location)
                this_region.append(next)

                x = next_x
                y = next_y

        regions.append((plant, this_region))

print(regions)
