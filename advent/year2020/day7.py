import re
from collections import defaultdict

OUTER_PATTEN = re.compile(r"^([a-z ]+) bags contain")
INNER_PATTERN = re.compile(r"(\d+) ([a-z ]+) bag")


def read_input():
    with open('input/2020/day7-input.txt', encoding='utf-8') as file:
        return parse(file.read())


def parse(text):
    bags = {}

    for line in text.strip().split("\n"):
        match = OUTER_PATTEN.match(line)
        key = match.group(1)
        bags[key] = [(int(count), colour) for count, colour in INNER_PATTERN.findall(line)]

    return bags


def part1(data):
    """
    >>> part1(read_input())
    254
    """

    reverse = defaultdict(list)

    for colour, bags in data.items():
        for (_, bag) in bags:
            reverse[bag].append(colour)

    queue = ['shiny gold']
    colours = set()

    while queue:
        colour = queue.pop(0)

        for colour in reverse[colour]:
            if colour not in colours:
                colours.add(colour)
                queue.append(colour)

    return len(colours)


def bag_count(bags, bag_colour):
    return 1 + sum(count * bag_count(bags, colour) for (count, colour) in bags[bag_colour])


def part2(bags):
    """
    >>> data = parse("light red bags contain 1 bright white bag, 2 muted yellow bags.\\n" +
    ...     "dark orange bags contain 3 bright white bags, 4 muted yellow bags.\\n" +
    ...     "bright white bags contain 1 shiny gold bag.\\n" +
    ...     "muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.\\n" +
    ...     "shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.\\n" +
    ...     "dark olive bags contain 3 faded blue bags, 4 dotted black bags.\\n" +
    ...     "vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.\\n" +
    ...     "faded blue bags contain no other bags.\\ndotted black bags contain no other bags.")
    >>> part2(data)
    32
    >>> part2(read_input())
    6006
    """

    # Don't count the shiny gold bag itself
    return bag_count(bags, 'shiny gold') - 1


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
