input = "2333133121414131402"
# input = "12345"

files = []
free_spaces = []

for i in range(0, len(input), 2):
    file_block = int(input[i])
    free_space = int(input[i + 1]) if i + 1 < len(input) else None
    files.append(file_block)
    free_spaces.append(free_space)


# Convert to blocks
blocks = []
for id, fileSize in enumerate(files):
    for i in range(fileSize):
        blocks.append(id)
    if id < len(free_spaces) and free_spaces[id]:
        for i in range(free_spaces[id]):
            blocks.append(None)


print(blocks)


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
