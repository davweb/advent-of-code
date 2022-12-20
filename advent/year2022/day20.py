# -*- coding: utf-8 -*-

from collections import deque


def read_input():
    with open('input/2022/day20-input.txt', encoding='utf8') as file:
        return [int(line) for line in file]


def mix(numbers, count=1):
    """
    >>> mix([1, 2, -3, 3, -2, 0, 4])
    [1, 2, -3, 4, 0, 3, -2]
    """

    size = len(numbers)
    queue = deque(range(size))

    for _ in range(count):
        for index in range(size):
            rotate = -queue.index(index)

            if rotate == 0:
                head = queue[1]
            else:
                head = queue[0]

            queue.rotate(rotate)
            queue.popleft()

            queue.rotate(-numbers[index])
            queue.appendleft(index)
            queue.rotate(-queue.index(head))

    return list(numbers[index] for index in queue)


def get_coordinate(data):
    zero = data.index(0)
    size = len(data)
    return sum(data[(zero + index) % size] for index in (1000, 2000, 3000))


def part1(data):
    """
    >>> part1(read_input())
    3466
    """

    data = mix(data)
    return get_coordinate(data)


def part2(data):
    """
    >>> part2(read_input())
    9995532008348
    """

    data = [811589153 * i for i in data]
    data = mix(data, 10)
    return get_coordinate(data)


def main():
    print(part1(read_input()))
    print(part2(read_input()))


if __name__ == "__main__":
    main()
