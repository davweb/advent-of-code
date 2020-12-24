# -*- coding: utf-8 -*-


def moves_for_line(line):
    steps = []
    previous = None

    for c in line:
        if c in ['n', 's']:
            if previous is not None:
                raise ValueError()
            previous = c

        elif c in ['e', 'w']:
            if previous is None:
                steps.append(c)
            else:
                steps.append("{}{}".format(previous, c))

            previous = None

    return steps


def read_input():
    file = open("input/2020/day24-input.txt", "r")
    return [moves_for_line(line) for line in file]


def direction_for_location(location, direction):
    _, y = location

    if direction == 'e':
        return (1, 0)
    elif direction == 'w':
        return (-1, 0)
    elif direction == 'se':
        if y % 2 == 0:
            return (0, -1)
        else:
            return (1, -1)
    elif direction == 'sw':
        if y % 2 == 0:
            return (-1, -1)
        else:
            return (0, -1)
    elif direction == 'ne':
        if y % 2 == 0:
            return (0, 1)
        else:
            return (1, 1)
    elif direction == 'nw':
        if y % 2 == 0:
            return (-1, 1)
        else:
            return (0, 1)


def move(location, direction):
    """
    >>> location = (0, 0)
    >>> for direction in moves_for_line('nwwswee'):
    ...     location = move(location, direction)
    >>> location
    (0, 0)
    >>> for direction in moves_for_line('esew'):
    ...     location = move(location, direction)
    >>> location
    (0, -1)
    """

    dx, dy = direction_for_location(location, direction)
    x, y = location
    return (x + dx, y + dy)


def set_up(moves):
    black = set()

    for steps in moves:
        location = (0, 0)

        for direction in steps:
            location = move(location, direction)

        if location in black:
            black.remove(location)
        else:
            black.add(location)

    return black


def part1(moves):
    """
    >>> part1(read_input())
    244
    """

    return len(set_up(moves))


def adjacent(location):
    """
    >>> adjacent((0, 0))
    [(1, 0), (-1, 0), (0, 1), (-1, 1), (0, -1), (-1, -1)]
    >>> adjacent((5, 8))
    [(6, 8), (4, 8), (5, 9), (4, 9), (5, 7), (4, 7)]
    >>> adjacent((5, 7))
    [(6, 7), (4, 7), (6, 8), (5, 8), (6, 6), (5, 6)]
    """
    return [move(location, direction) for direction in ['e', 'w', 'ne', 'nw', 'se', 'sw']]


def part2(moves):
    """
    >>> part2(read_input())
    3665
    """

    black = set_up(moves)
    day = 0

    while day < 100:
        day += 1
        in_play = black.copy()

        for location in black:
            in_play.update(adjacent(location))

        new = set()

        for location in in_play:
            is_black = location in black
            black_count = len(black.intersection(adjacent(location)))

            if (is_black and 1 <= black_count <= 2) or (not is_black and black_count == 2):
                new.add(location)

        black = new

    return len(black)


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
