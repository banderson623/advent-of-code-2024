import os

input = "2333133121414131402"
# input = "12345"

input_file_path = os.path.join(os.path.dirname(__file__), "input.txt")
with open(input_file_path, "r") as f:
    input = f.read().strip()

blocks = []


file_size_by_id = []

# Parse input and build blocks
for i in range(0, len(input), 2):
    fileSize = int(input[i])
    freeSize = int(input[i + 1]) if i + 1 < len(input) else None
    file_size_by_id.append(fileSize)

    for id in range(fileSize):
        file_id = int(i / 2)
        blocks.append(file_id)

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

    # print("")
    # print("vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv")
    print(string)
    # print("01234567890123456789012345678901234567890123456789")
    # print("          1         2         3         4")
    # print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    # print("")


prettyPrintBlocks(blocks)


def find_empty_chunks(blocks):
    empty_chunks = []

    empty_size = 0
    starts_index = None
    for i, block in enumerate(blocks):
        if block is None:
            if starts_index is None:
                starts_index = i
            empty_size += 1
        else:
            if starts_index is not None:
                empty_chunks.append((starts_index, empty_size))
                starts_index = None
                empty_size = 0

    if starts_index is not None:
        empty_chunks.append((starts_index, empty_size))

    return empty_chunks


# COMPACTING TIME ------------------------------
# lets walk down this backwards
already_seen_down_to_location = len(blocks)


for location in range(len(blocks) - 1, 0, -1):

    # I didn't know how to modify the location, so we can
    # just skip this whole section if we already analyzed this
    if location > already_seen_down_to_location:
        continue

    print(location)

    file_id = blocks[location]

    if file_id is not None:
        file_size = file_size_by_id[file_id]

        empty_chunks = find_empty_chunks(blocks)
        # print(f"checking if I can put {file_id} (size: {file_size}) somewhere here -> empty chunks {empty_chunks}")
        for empty_index, size in empty_chunks:
            if size >= file_size and empty_index < location:
                for i in range(0, file_size):
                    blocks[empty_index + i] = file_id
                    blocks[location - i] = None

                # prettyPrintBlocks(blocks)
                break

        # We analyzed this, lets go....
        already_seen_down_to_location = location - file_size

prettyPrintBlocks(blocks)

# CHECKSOME TIME
checksum = 0
for i, file_id in enumerate(blocks):
    if file_id is not None:
        checksum += i * file_id

print(f"checksum: {checksum}")
