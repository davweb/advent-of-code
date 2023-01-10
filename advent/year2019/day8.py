#!/usr/local/bin/python3

from collections import defaultdict
from operator import itemgetter


def read_input():
    with open('input/2019/day8-input.txt', encoding='utf-8') as file:
        return [int(digit) for digit in file.read()]


def count_pixels(input_value, width, height):
    """
    >>> data = (0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 0)
    >>> count = count_pixels(data, 3, 2)
    >>> count[0][0]
    3
    >>> count[1][0]
    3
    >>> count[1][1]
    3
    >>> count[2][0]
    0
    >>> count[2][1]
    2
    """

    layer_size = width * height
    count = defaultdict(lambda: defaultdict(int))
    index = 0
    layer = 0

    for digit in input_value:
        count[digit][layer] += 1

        index += 1
        if index % layer_size == 0:
            layer += 1

    return count


def image(data, width, height):
    pixels = [[2 for x in range(0, width)] for y in range(0, height)]
    x = 0
    y = 0

    for pixel in data:
        if pixels[y][x] == 2:
            pixels[y][x] = pixel

        x += 1
        if x >= width:
            x = 0
            y += 1

            if y >= height:
                y = 0

    return "\n".join("".join("█" if pixel else " " for pixel in row) for row in pixels)


def key_for_smallest_value(some_dict):
    return min(some_dict.items(), key=itemgetter(1))[0]


def part1(data):
    """
    >>> part1(read_input())
    1965
    """

    count = count_pixels(data, 25, 6)
    layer = key_for_smallest_value(count[0])
    return count[1][layer] * count[2][layer]


def part2(data):
    """
    >>> from advent import md5
    >>> md5(part2(read_input()))
    '70918ebfcb8099bc4cc51de972a09319'
    """

    return image(data, 25, 6)


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
