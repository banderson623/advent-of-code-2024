import os

input = """
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""

input_file_path = os.path.join(os.path.dirname(__file__), "input.txt")
with open(input_file_path, "r") as f:
    input = f.read()


[rules_text, update_list] = input.strip().split("\n\n")

rules = []

for rule in rules_text.split("\n"):
    rules.append(rule.split("|"))


def is_valid_update(pages):
    for before, after in rules:
        if before in pages and after in pages:
            if pages.index(before) > pages.index(after):
                return False
    return True


def correctly_ordered_pages(pages):
    while not is_valid_update(pages):
        for before, after in rules:
            if before in pages and after in pages:
                if pages.index(before) > pages.index(after):
                    # swap the locations of before and after
                    pages[pages.index(before)] = after
                    pages[pages.index(after)] = before

    return pages


sum_of_fixed_middles = 0
for updates in update_list.split("\n"):
    pages = updates.split(",")
    if not is_valid_update(pages):
        pages = correctly_ordered_pages(pages)
        sum_of_fixed_middles += int(pages[len(pages) // 2])

print(sum_of_fixed_middles)
