import advent

INPUT = 'jxqlasbh'


def read_input():
    data = []

    for row in range(0, 128):
        seed = "%s-%d" % (INPUT, row)
        hash = advent.knot_hash(seed)
        hash = "".join("{0:08b}".format(value) for value in hash)
        hash = [int(c) for c in hash]
        data.append(hash)

    return data


def find_first(data):
    """
    >>> find_first([[0, 0], [0, 1]])
    (1, 1)
    >>> find_first([[0, 0], [0, 0]])
    """

    for y in range(0, len(data)):
        for x in range(0, len(data[y])):
            if data[y][x] == 1:
                return (x, y)

    return None


def zero(data, x, y):
    if x < 0 or y < 0:
        return

    try:
        if data[y][x] == 0:
            return
    except IndexError:
        return

    data[y][x] = 0

    zero(data, x - 1, y)
    zero(data, x, y - 1)
    zero(data, x + 1, y)
    zero(data, x, y + 1)


def part1(data):
    """
    >>> part1(read_input())
    8140
    """

    return sum(sum(row) for row in data)


def part2(data):
    """
    >>> part2(read_input())
    1182
    """

    c = find_first(data)
    count = 0

    while c is not None:
        count += 1
        x, y = c
        zero(data, x, y)
        c = find_first(data)

    return count


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
