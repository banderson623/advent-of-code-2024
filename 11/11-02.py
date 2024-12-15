from functools import lru_cache
import os

input = "125 17"

input_file_path = os.path.join(os.path.dirname(__file__), "input.txt")
with open(input_file_path, "r") as f:
    input = f.read().strip()

stones = input.strip().split(" ")


seen_results = {}

cache_hits = 0
cache_miss = 0

# I wanted to learn how to do this myself, so I commented out the better
# wan to do this, for the sake of learning


# @lru_cache(maxsize=None)
def stone_evolution_counter(stone, remaining_evolutions):
    global cache_hits, cache_miss

    if (stone, remaining_evolutions) in seen_results:
        cache_hits += 1
        return seen_results[(stone, remaining_evolutions)]

    cache_miss += 1
    if remaining_evolutions == 0:
        # there is no more evolutions this stone is the final stone, so count 1
        return 1

    if stone == "0":
        # lets keep recursing, after transform this to 1, and reduce the evolutions
        count = stone_evolution_counter("1", remaining_evolutions - 1)
        seen_results[(stone, remaining_evolutions)] = count
        return count

    if len(stone) % 2 == 0:
        left = str(int(stone[: len(stone) // 2]))
        right = str(int(stone[len(stone) // 2 :]))
        # this will recurse down both sides, and do it separately. Importantly, it makes heavy use
        # of the cache function so we only need to trace down each number at each remaining evolution
        # once. This WILL NOT WORK without the cache.
        count = stone_evolution_counter(left, remaining_evolutions - 1) + stone_evolution_counter(
            right, remaining_evolutions - 1
        )
        seen_results[(stone, remaining_evolutions)] = count
        return count
    else:
        # okay, well this is the case where we now will multiply the number by 2024
        count = stone_evolution_counter(str(int(stone) * 2024), remaining_evolutions - 1)
        seen_results[(stone, remaining_evolutions)] = count
        return count


stone_count = 0

for stone in stones:
    stone_count += stone_evolution_counter(stone, 25)

print("number of stones (25)", stone_count)
print("cache hits", cache_hits)
print("cache miss", cache_miss)
print(f"ratio {round(cache_hits / cache_miss * 100, 2)}%")

stone_count = 0
cache_hits = 0
cache_miss = 0
for stone in stones:
    stone_count += stone_evolution_counter(stone, 75)

print("number of stones (75)", stone_count)
print("cache hits", cache_hits)
print("cache miss", cache_miss)
print(f"ratio {round(cache_hits / cache_miss * 100, 2)}%")


stone_count = 0
cache_hits = 0
cache_miss = 0
for stone in stones:
    stone_count += stone_evolution_counter(stone, 500)

print("number of stones (500)", stone_count)
print("cache hits", cache_hits)
print("cache miss", cache_miss)
print(f"ratio {round(cache_hits / cache_miss * 100, 2)}%")
