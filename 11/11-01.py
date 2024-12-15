input = "125 17"

import os

input_file_path = os.path.join(os.path.dirname(__file__), "input.txt")
with open(input_file_path, "r") as f:
    input = f.read().strip()

stones = input.strip().split(" ")


def evolve(stones):
    next_stones = []

    for i, stone in enumerate(stones):
        if stone == "0":
            next_stones.append("1")
        elif len(stone) % 2 == 0:
            # little bit of extra here, as I need to trim the leading zeros
            # which was easiest converting to integers before back to strings
            next_stones.append(str(int(stone[: len(stone) // 2])))
            next_stones.append(str(int(stone[len(stone) // 2 :])))
        else:
            next_stones.append(str(int(stone) * 2024))

    return next_stones


print(f"Start    and I have {str(len(stones)).rjust(6)} stones")
print("---------------------------------")
for i in range(25):
    stones = evolve(stones)
    print(f"Blink {str(i + 1).rjust(2)} and I have {str(len(stones)).rjust(6)} stones")
    # print(stones)

print("number of stones", len(stones))
