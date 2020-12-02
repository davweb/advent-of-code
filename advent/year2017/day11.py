
DIRECTIONS = {
    'n': (0,2),
    'ne': (1,1),
    'se': (1,-1),
    's': (0,-2),
    'sw': (-1,-1),
    'nw': (-1,1)
}


def read_input():
    file = open('input/2017/day11-input.txt', 'r')
    return file.read().split(',')


def distance_home(x, y):
    """
    >>> distance_home(0, 0)
    0
    >>> distance_home(3, 3)
    3
    >>> distance_home(-3, 3)
    3
    >>> distance_home(0, 8)
    4
    """

    x,y = abs(x),abs(y)
    steps = 0

    while x != 0 or y != 0:
        if y > x:
            y -= 2
            steps += 1
        elif y < x:
            x -= 2
            steps += 2
        else:
            x -= 1
            y -= 1
            steps += 1

    return steps


def part1and2(data):
    """
    >>> part1and2(read_input())
    (664, 1447)
    """

    x, y = 0,0
    furthest = 0

    for move in data:
        dx,dy = DIRECTIONS[move]
        x += dx
        y += dy
        furthest = max(furthest, distance_home(x,y))

    return (distance_home(x,y), furthest)


def main():
    data = read_input()
    print(part1and2(data))


if __name__ == "__main__":
    main()