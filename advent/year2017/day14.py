import advent

INPUT = 'jxqlasbh'

def read_input():
    map = []

    for row in range(0,128):
        seed = "%s-%d" % (INPUT, row)
        hash = advent.knot_hash(seed)
        hash = "".join("{0:08b}".format(value) for value in hash)
        hash = [int(c) for c in hash]
        map.append(hash)

    return map


def find_first(map):
    """
    >>> find_first([[0, 0], [0, 1]])
    (1, 1)
    >>> find_first([[0, 0], [0, 0]])
    """

    for y in range(0, len(map)):
        for x in range(0, len(map[y])):
            if map[y][x] == 1:
                return (x,y)

    return None
 
 
def zero(map, x, y):
    if x < 0 or y < 0:
        return

    try:
        if map[y][x] == 0:
            return
    except IndexError:
        return

    map[y][x] = 0

    zero(map, x - 1, y)
    zero(map, x, y - 1)
    zero(map, x + 1, y)
    zero(map, x, y + 1)
 

def part1(map):
    """
    >>> part1(read_input())
    8140
    """

    return sum(sum(row) for row in map)


def part2(map):
    """
    >>> part2(read_input())
    1182
    """

    c = find_first(map)
    count = 0

    while c is not None:
        count += 1
        x,y = c
        zero(map, x, y)
        c = find_first(map)

    return count


def main():
    map = read_input()
    print(part1(map))
    print(part2(map))


if __name__ == "__main__":
    main()
