import os

input = "2333133121414131402"
input = "1311399"
# input = "12345"

input_file_path = os.path.join(os.path.dirname(__file__), "input.txt")
with open(input_file_path, "r") as f:
    input = f.read().strip()

files = {}
empties = {}


def prettyPrintBlocks(blocks, filename=None):
    string = ""
    for block in blocks:
        if block is None:
            string += "."
        else:
            string += str(block)

    print(string)
    if filename is not None:
        block_path = os.path.join(os.path.dirname(__file__), filename)
        with open(block_path, "w") as f:
            f.write(string)


# Parse input and build blocks
global_index = 0
for i in range(0, len(input), 2):
    fileSize = int(input[i])
    freeSize = int(input[i + 1]) if i + 1 < len(input) else None

    files[global_index] = {"size": fileSize, "id": int(i / 2)}
    global_index += fileSize

    empties[global_index] = freeSize if freeSize is not None else 0
    global_index += freeSize if freeSize is not None else 0


def blocks_from_files(files):
    # Set this with a lots of None
    blocks = [None] * global_index

    files = dict(sorted(files.items()))
    for block_index in files:
        file = files[block_index]

        for id in range(file["size"]):
            blocks[block_index + id] = file["id"]

    return blocks


print(input)
prettyPrintBlocks(blocks_from_files(files), "start.txt")


compacted = {}

# the strategy is to walk the reverse files and try to fit them in the empty spaces
for block_index in reversed(files):
    file = files[block_index]

    # let's see if this will fit in an empty space
    for empty_index, empty_size in empties.items():

        # lets not consider indices larger than this block index
        if empty_index > block_index:
            continue

        file_fits = empty_size >= file["size"]
        if file_fits:
            empties.pop(empty_index)
            files[block_index]["moved"] = True

            remainder = empty_size - file["size"]
            compacted[empty_index] = file

            # If we have a remainder we need to account for this in the empties
            if remainder > 0:
                new_empty_index = empty_index + file["size"]
                empties[new_empty_index] = remainder

            break


# Now move all of the non compacted files into the compacted space
for file_index in files:
    if "moved" not in files[file_index]:
        compacted[file_index] = files[file_index]


blocks = blocks_from_files(compacted)
prettyPrintBlocks(blocks, "compacted.txt")

# CHECKSOME TIME
checksum = 0
for i, file_id in enumerate(blocks):
    if file_id is not None:
        checksum += i * file_id

print(f"checksum: {checksum}")
