import os

input = "2333133121414131402"

input_file_path = os.path.join(os.path.dirname(__file__), "input.txt")
with open(input_file_path, "r") as f:
    input = f.read().strip()

blocks = []

# Parse input and build blocks
for i in range(0, len(input), 2):
    fileSize = int(input[i])
    freeSize = int(input[i + 1]) if i + 1 < len(input) else None

    for id in range(fileSize):
        blocks.append(int(i / 2))

    if freeSize is not None:
        for id in range(freeSize):
            blocks.append(None)


def prettyPrintBlocks(blocks):
    string = ""
    for block in blocks:
        if block is None:
            string += "."
        else:
            string += str(block)

    print(string)


prettyPrintBlocks(blocks)


# COMPACTING TIME ------------------------------
# lets walk down this backwards
for location in range(len(blocks) - 1, 0, -1):
    next_empty_index = blocks.index(None)

    if next_empty_index >= location:
        break

    blocks[next_empty_index] = blocks[location]
    blocks[location] = None


prettyPrintBlocks(blocks)

# CHECKSOME TIME
checksum = 0
for i, file_id in enumerate(blocks):
    if file_id is not None:
        checksum += i * file_id

print(f"checksum: {checksum}")
