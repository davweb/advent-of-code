# -*- coding: utf-8 -*-

from collections import defaultdict


def read_input(filename='input/2025/day7-input.txt'):
    grid = {}

    with open(filename, encoding='utf8') as file:
        for y, line in enumerate(file.readlines()):
            for x, c in enumerate(line.strip()):
                if c != '.':
                    grid[(x, y)] = c

    return grid


def part1(grid):
    """
    >>> part1(read_input())
    1562
    """

    start = next(location for location, cell in grid.items() if cell == 'S')
    max_y = max(y for _, y in grid.keys())

    queue = [start]
    del grid[start]

    splits = 0

    while queue:
        (x, y) = queue.pop()

        match grid.get((x, y), '.'):
            case '|':
                continue
            case '.':
                grid[(x, y)] = '|'
                if y <= max_y:
                    queue.append((x, y + 1))
            case '^':
                splits += 1
                queue.append((x + 1, y))
                queue.append((x - 1, y))
            case _:
                raise ValueError()

    return splits


def part2(grid):
    """
    >>> part2(read_input())
    24292631346665
    """

    start = next(location for location, cell in grid.items() if cell == 'S')
    max_y = max(y for _, y in grid.keys())

    queue = [start]
    del grid[start]

    fake = (-1, -1)
    counts = {fake: 1}
    parents = defaultdict(set)
    parents[start].add(fake)

    while queue:
        queue.sort(key=lambda l: l[1])
        location = queue.pop(0)
        counts[location] = sum(counts[p] for p in parents[location])
        x, y = location

        match grid.get(location, '.'):
            case '|':
                continue
            case '.':
                grid[(x, y)] = '|'
                if y <= max_y:
                    queue.append((x, y + 1))
                    parents[(x, y + 1)].add(location)
            case '^':
                queue.append((x + 1, y))
                queue.append((x - 1, y))
                parents[(x + 1, y)].add(location)
                parents[(x - 1, y)].add(location)
            case _:
                raise ValueError()

    return sum(count for (_, y), count in counts.items() if y == max_y + 1)


def main():
    print(part1(read_input()))
    print(part2(read_input()))


if __name__ == "__main__":
    main()
