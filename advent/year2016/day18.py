# -*- coding: utf-8 -*-

INPUT = '.^^^.^.^^^.^.......^^.^^^^.^^^^..^^^^^.^.^^^..^^.^.^^..^.^..^^...^.^^.^^^...^^.^.^^^..^^^^.....^....'
TRAP = '^'
SAFE = '.'


def next_line(line):
    """
    >>> next_line('..^^.')
    '.^^^^'
    >>> next_line('.^^.^.^^^^')
    '^^^...^..^'
    """

    # Its left and center tiles are traps, but its right tile is not.
    # Its center and right tiles are traps, but its left tile is not.
    # Only its left tile is a trap.
    # Only its right tile is a trap.


    output = ''
    line = f'{line}{SAFE}'
    left = False
    centre = line[0] == TRAP

    for char in line[1:]:
        right = char == TRAP

        match left, centre, right:
            case True, True, False:
                next_char = TRAP
            case False, True, True:
                next_char = TRAP
            case True, False, False:
                next_char = TRAP
            case False, False, True:
                next_char = TRAP
            case _:
                next_char = SAFE

        output += next_char
        left, centre = centre, right

    return output


def count_safe_tiles(line, limit):
    count = 0

    for _ in range(limit):
        count += sum(c == SAFE for c in line)
        line = next_line(line)

    return count


def part1(line):
    """
    >>> part1(INPUT)
    2013
    """

    return count_safe_tiles(line, 40)


def part2(line):
    """
    >>> part2(INPUT)
    20006289
    """

    return count_safe_tiles(line, 400000)


def main():
    print(part1(INPUT))
    print(part2(INPUT))


if __name__ == "__main__":
    main()
