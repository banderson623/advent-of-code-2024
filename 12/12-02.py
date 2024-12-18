# Commentary on the strategy:
# I tried a lot of things to get this to work. Perimeter is easier.
# Wall counting requires a lot of bookkeeping. And roughly finding a perimeter, and
# walking along it (both directions), until you end of out perimeter (aka it changes direction)
# you also need to keep track of the wall parts you've walked along so you don't double count.

# I'm sure this could be optimized.

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

# input = """
# EEEEE
# EXXXX
# EEEEE
# EXXXX
# EEEEE"""

input = """
AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA"""

input = """
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""


# import os

# input_file_path = os.path.join(os.path.dirname(__file__), "input.txt")
# with open(input_file_path, "r") as f:
#     input = f.read().strip()

map = []
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


DIRECTIONS = {"w": (-1, 0), "e": (1, 0), "s": (0, 1), "n": (0, -1)}


def walls_for_the_region(region):
    wall_count = 0
    plant_type, locations = region

    if len(locations) == 1:
        return 4
    if len(locations) == 2:
        return 4

    log_plants = []

    perimeter_directions = {}

    region_vertical_steps = abs(
        max([location[1] for location in locations]) - min([location[1] for location in locations])
    )
    region_horizontal_steps = abs(
        max([location[0] for location in locations]) - min([location[0] for location in locations])
    )
    # print(f"max steps vertical:{region_vertical_steps}, horizontal:{region_horizontal_steps}")

    for plant_location in locations:
        x, y = plant_location
        perimeters = set()

        all_neighbor_perimeters = set()

        # Look around in each direction
        # 1. Determine if i have a neighbor in this direction
        # 2. Record that i have a neightbor in this direction
        # 3. Determine if my neighbor has a perimeter in this direction
        # 4. If not, then i have a wall in this direction
        for direction in DIRECTIONS:
            neighbor_location = (x + DIRECTIONS[direction][0], y + DIRECTIONS[direction][1])

            # Determine my own perimeter
            if neighbor_location not in locations:
                perimeters.add(direction)

        # print(f"Perimeters for {plant_location} are {perimeters}")
        perimeter_directions[plant_location] = perimeters

    if plant_type in log_plants:
        print(f"Perimeters for {plant_type}: {perimeter_directions}")

    # okay now we have every permitter for each plant location
    # lets start in the top left and trace each wall
    # we'll keep track of the walls we've already counted so we don't double count
    counted_locations_and_direction = set()
    walls = set()

    for plant_location in locations:
        x, y = plant_location

        # if plant_type in log_plants:
        #     print(f"Checking location {plant_location}, {perimeter_directions[plant_location]}")

        for direction in perimeter_directions[plant_location]:
            wall_friends = set()
            if direction in ["w", "e"]:
                for walk_direction in [1, -1]:
                    # if plant_type in log_plants:
                    #     print(
                    #         f" ^v Checking along the {direction} for {plant_location}, moving vertical, stepping {walk_direction}"
                    #     )

                    for i in range(0, walk_direction * (region_vertical_steps + 1), walk_direction):
                        checking_location = (x, y + i)

                        # if plant_type in log_plants:
                        #     print(f"checking {direction} {checking_location}")

                        if checking_location in locations and direction in perimeter_directions[checking_location]:
                            # if plant_type in log_plants:
                            #     print(f"found a wall friend", (direction, checking_location))
                            if (direction, checking_location) not in counted_locations_and_direction:
                                wall_friends.add((direction, checking_location))
                            counted_locations_and_direction.add((direction, checking_location))
                        else:
                            # no more shared perimeter neighbors found, abort
                            break

            if direction in ["n", "s"]:

                for walk_direction in [1, -1]:
                    if plant_type in log_plants:
                        print(
                            f" <==> Checking along the {direction} for {plant_location}, moving horizontal, stepping {walk_direction}"
                        )

                    for i in range(0, walk_direction * (region_horizontal_steps + 1), walk_direction):

                        checking_location = (x + i, y)
                        if plant_type in log_plants:
                            print(f"  {i}  <==> {checking_location}")

                        if checking_location in locations and direction in perimeter_directions[checking_location]:
                            # if plant_type in log_plants:
                            #     print(f"found a wall friend", (direction, checking_location))

                            if (direction, checking_location) not in counted_locations_and_direction:
                                wall_friends.add((direction, checking_location))

                            counted_locations_and_direction.add((direction, checking_location))
                        else:
                            if plant_type in log_plants:
                                print(f"no more shared perimeter neighbors found, abort")
                            # no more shared perimeter neighbors found, abort
                            break

            if len(wall_friends) > 0:
                walls.add(frozenset(wall_friends))

                if plant_type in log_plants:
                    print(f"found walls", wall_friends)
                    print(f"counted locations and directions", counted_locations_and_direction)

    if plant_type in log_plants:
        print(f"Walls for region: {walls}")

    # print(perimeter_directions)
    # print(f"Perimeter directions: {perimeter_directions}")
    wall_count = len(walls)
    return wall_count


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
print(input)
for region in regions:
    plant, locations = region
    # perimiter = perimeter_for_the_region(region)
    # print()
    # print(f"==== {plant} ====")
    wall_count = walls_for_the_region(region)
    area = len(locations)
    price = area * wall_count
    total_cost += price
    print(f"Walls for {plant} is {wall_count}, area {area} - price ${price}")

print("total cost: $", total_cost)
