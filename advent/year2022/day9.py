# -*- coding: utf-8 -*-

def read_input():
    output = []

    with open('input/2022/day9-input.txt', encoding='utf8') as file:
        for line in file.readlines():
            direction, distance = line.split()
            output.append((direction, int(distance)))

    return output


def step(head, tail):
    if head > tail:
        return tail + 1

    if head < tail:
        return tail - 1

    return tail


def pull_rope(head, tail):
    mx = abs(head[0] - tail[0])
    my = abs(head[1] - tail[1])

    if mx > 1 or my > 1 or (mx + my) > 2:
        return (step(head[0], tail[0]), step(head[1], tail[1]))
    else:
        return tail


def move(head, direction):
    match direction:
        case 'U':
            return (head[0], head[1] + 1)
        case 'D':
            return (head[0], head[1] - 1)
        case 'L':
            return (head[0] - 1, head[1])
        case 'R':
            return (head[0] + 1, head[1])
        case _:
            raise ValueError()


def part1(data):
    """
    >>> part1(read_input())
    6563
    """

    head = (0, 0)
    tail = (0, 0)
    visited = set([tail])

    for direction, distance in data:
        for _ in range(distance):
            head = move(head, direction)
            tail = pull_rope(head, tail)
            visited.add(tail)

    return len(visited)


def part2(data):
    """
    >>> part2(read_input())
    2653
    """

    rope = [(0, 0)] * 10
    visited = set([rope[-1]])

    for direction, distance in data:
        for _ in range(distance):
            head = move(rope[0], direction)
            new_rope = [head]

            for tail in rope[1:]:
                head = pull_rope(head, tail)
                new_rope.append(head)

            visited.add(head)
            rope = new_rope

    return len(visited)


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
