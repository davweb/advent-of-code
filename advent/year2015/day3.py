def read_input():
    with open('input/2015/day3-input.txt', encoding='utf8') as file:
        return file.read()


def move(location, direction):
    (x, y) = location

    if direction == '>':
        x += 1
    elif direction == '<':
        x -= 1
    elif direction == '^':
        y += 1
    elif direction == 'v':
        y -= 1
    else:
        raise ValueError(direction)

    return (x, y)


def part1(data):
    """
    >>> part1(">")
    2
    >>> part1("^v^v^v^v^v")
    2
    >>> part1("^>v<")
    4
    >>> part1(read_input())
    2572
    """

    santa = (0, 0)
    visited = set([santa])

    for d in data:
        santa = move(santa, d)
        visited.add(santa)

    return len(visited)


def part2(data):
    """
    >>> part2("^v")
    3
    >>> part2("^v^v^v^v^v")
    11
    >>> part2("^>v<")
    3
    >>> part2(read_input())
    2631
    """

    santa = (0, 0)
    other = (0, 0)
    visited = set([santa])

    for d in data:
        santa = move(santa, d)
        visited.add(santa)
        santa, other = other, santa

    return len(visited)


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
