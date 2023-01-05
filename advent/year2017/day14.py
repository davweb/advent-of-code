import advent

INPUT = 'jxqlasbh'


def read_input():
    data = []

    for row in range(0, 128):
        seed = f'{INPUT}-{row}'
        hash_value = advent.knot_hash(seed)
        hash_value = ''.join(f'{value:08b}' for value in hash_value)
        hash_value = [int(c) for c in hash_value]
        data.append(hash_value)

    return data


def find_first(data):
    """
    >>> find_first([[0, 0], [0, 1]])
    (1, 1)
    >>> find_first([[0, 0], [0, 0]])
    """

    for y_index, y_value in enumerate(data):
        for x_index, x_value in enumerate(y_value):
            if x_value == 1:
                return (x_index, y_index)

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
