input = """
AAAA
BBCD
BBCC
EEEC
"""

# input = """OOOOO
# OXOXO
# OOOOO
# OXOXO
# OOOOO"""

# input = """
# RRRRIICCFF
# RRRRIICCCF
# VVRRRCCFFF
# VVRCCCJFFF
# VVVVCJJCFE
# VVIVCCJJEE
# VVIIICJJEE
# MIIIIIJJEE
# MIIISIJEEE
# MMMISSJEEE"""


import os

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

# lets find contiguous plant regions:
# 1. Use a recursive function to collect all the plants in a region that touch.
# 2. We'll loop through this for each plant type until all the plants are placed
#    in a region

regions = []


def find_all_all_plants_in_region(all_locations_of_this_plant, starting_location, discovered_plants=[]):
    plants_discovered_in_walk = []
    plants_discovered_in_walk.append(starting_location) if starting_location not in discovered_plants else None

    discovered_plants.append(starting_location)

    x, y = starting_location

    # now look around up, right, down, left
    for next in [(x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)]:
        # if this is on the board...
        if next[0] >= 0 and next[0] < len(map[0]) and next[1] >= 0 and next[1] < len(map):
            # ... and this a location of this plant, AND we haven't already found it...
            if next in all_locations_of_this_plant and next not in discovered_plants:
                # move to this location and do the same
                plant_locations = find_all_all_plants_in_region(all_locations_of_this_plant, next, discovered_plants)
                # and now add them to our location
                for new_plant_in_region in plant_locations:
                    plants_discovered_in_walk.append(new_plant_in_region)

    return plants_discovered_in_walk


def perimeter_for_the_region(region):
    perimeter = 0
    locations = region[1]
    for plant_location in locations:
        x, y = plant_location
        for next in [(x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)]:
            # whatever side doesn't have a neighbor requires a fence (counts as a perimeter)
            perimeter += 1 if next not in locations else 0
    return perimeter


# the main part of the program
for plant in plant_locations:
    plants_found = set()  # of locations
    all_locations_of_this_plant = plant_locations[plant]

    while len(plants_found) < len(all_locations_of_this_plant):
        # the first location_of_this_plant that does not exist in plants_found
        starting_location = next(loc for loc in all_locations_of_this_plant if loc not in plants_found)

        region = find_all_all_plants_in_region(all_locations_of_this_plant, starting_location)
        for plant_location in region:
            plants_found.add(plant_location)

        regions.append((plant, region))

total_cost = 0
for region in regions:
    plant, locations = region
    perimiter = perimeter_for_the_region(region)
    area = len(locations)
    price = area * perimiter
    total_cost += price
    print(f"Perimeter for {plant} is {perimiter}, area {area} - price ${price}")

print("total cost: $", total_cost)
