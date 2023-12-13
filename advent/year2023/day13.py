# -*- coding: utf-8 -*-


def read_input(filename='input/2023/day13-input.txt'):
    with open(filename, encoding='utf8') as file:
        diagrams = []
        diagram = []

        for line in file:
            line = line.strip()
            if line == "":
                diagrams.append(diagram)
                diagram = []
            else:
                diagram.append(line)

        diagrams.append(diagram)
        return diagrams


def find_in_diagram(diagram, compare_slices):
    for before in range(1, len(diagram)):
        after = len(diagram) - before
        size = min(before, after)

        left = diagram[before - size:before]
        right = diagram[before + size - 1:before - 1:-1]

        if compare_slices(left, right):
            return before

    return None


def find_reflection(diagram):
    """
    >>> find_reflection(('...','###','###'))
    2
    >>> find_reflection(('...','###','#.#','#.#','###'))
    3
    >>> find_reflection(('...','###','#.#','#.#','###','...','###','#.#','#.#'))
    3
    >>> find_reflection(('.#.','###','#.#','#.#','###','...','###','#.#','#.#'))
    8
    >>> find_reflection(('####....####.#.##', '.....#..#.#...#.#', '#......##..#.###.', \\
    ...    '...####.#.##.#...', '###...##.#..#.###', '###..###.#..#.###', '...####.#.##.#...', \\
    ...    '.#..#......#####.', '.#..#......#####.', '...####.#.##.#...', '###..###.#..#.###', \\
    ...    '###...##.#..#.###', '...####.#.##.#...'))
    8
    """

    return find_in_diagram(diagram, lambda left, right: left == right)


def find_smudge(diagram):
    """"
    >>> find_smudge(('...','#.#','###'))
    2
    >>> find_smudge(('####....####.#.##', '.....#..#.#...#.#', '#......##..#.###.', \\
    ...    '...####.#.##.#...', '###...##.#..#.###', '###..###.#..#.###', '...####.#.##.#...', \\
    ...    '.#..#......#####.', '.#..#......#####.', '...####.#.##.#...', '###..###.#..#.###', \\
    ...    '###...##.#..#.###', '...####.#.##.#...'))
    11
    """

    def single_difference(left, right):
        return sum(lc != rc for lr, rr in zip(left, right) for lc, rc in zip(lr, rr)) == 1

    return find_in_diagram(diagram, single_difference)


def solve(data, search_function):
    total = 0

    for diagram in data:
        top = search_function(diagram)

        if top is None:
            rotated = list(zip(*diagram))
            left = search_function(rotated)
            total += left
        else:
            total += 100 * top

    return total


def part1(data):
    """
    >>> part1(read_input())
    34100
    """

    return solve(data, find_reflection)


def part2(data):
    """
    >>> part2(read_input())
    33106
    """

    return solve(data, find_smudge)


def main():
    print(part1(read_input()))
    print(part2(read_input()))


if __name__ == "__main__":
    main()
