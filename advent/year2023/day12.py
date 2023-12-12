# -*- coding: utf-8 -*-


from functools import cache


def read_input(filename='input/2023/day12-input.txt'):
    with open(filename, encoding='utf8') as file:
        for line in file:
            springs, expected = line.split()
            yield springs, tuple(int(i) for i in expected.split(','))


@cache
def is_valid_group(spring):
    """
    Tests is this is a valid group followed by a gap

    >>> is_valid_group('.')
    False
    >>> is_valid_group('#')
    False
    >>> is_valid_group('..')
    False
    >>> is_valid_group('#.')
    True
    >>> is_valid_group('###.')
    True
    >>> is_valid_group('#.#.')
    False
    """

    return len(spring) > 1 and spring[-1] in ('?', '.') and all(c in ('?', '#') for c in spring[:-1])


@cache
def valid_count(springs, groups, depth=0):
    """
    >>> valid_count('.#.#.###.', (1, 1, 2))
    0
    >>> valid_count('.#.#.###.', (1, 1, 3))
    1
    >>> valid_count('#.#.###', (1, 1, 3))
    1
    >>> valid_count('#.?.###', (1, 1, 3))
    1
    >>> valid_count('#.?.?##?', (1, 1, 3))
    2
    >>> valid_count('?###????????', (3, 2, 1))
    10
    >>> valid_count('.#...??###?', (1, 5))
    2
    """

    if depth >= len(groups):
        return 1 if '#' not in springs else 0

    #  Add a space on the end to avoid the edge case of the group hitting the end of the string
    if depth == 0:
        springs += '.'

    expected_length = groups[depth] + 1
    remaining_length = sum(groups[depth:]) + len(groups[depth:]) - 1
    end = len(springs) - remaining_length
    total = 0
    i = 0

    while i < end:
        if is_valid_group(springs[i:i + expected_length]):
            total += valid_count(springs[i + expected_length:], groups, depth + 1)
        if springs[i] == '#':
            break
        i += 1

    return total


def part1(data):
    """
    >>> part1(read_input())
    7922
    """

    return sum(valid_count(springs, expected) for springs, expected in data)


def part2(data):
    """
    >>> part2(read_input())
    18093821750095
    """

    count = 0

    for springs, expected in data:
        springs = '?'.join([springs] * 5)
        expected *= 5
        count += valid_count(springs, expected)

    return count


def main():
    print(part1(read_input()))
    print(part2(read_input()))


if __name__ == "__main__":
    main()
