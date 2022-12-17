# -*- coding: utf-8 -*-

from itertools import cycle

SHAPES = [[60], [16, 56, 16], [56, 8, 8], [32, 32, 32, 32], [48, 48]]

EMPTY_ROW = 257
FULL_ROW = 511


def read_input():
    with open('input/2022/day17-input.txt', encoding='utf8') as file:
        return file.read().strip()


def first_filled_row(rows):
    index = len(rows) - 1

    while rows[index] == EMPTY_ROW:
        index -= 1

    return index


def drop_shapes(wind_data, max_shapes, find_repeat=False):
    """
    >>> drop_shapes(">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>", 2022)
    3068
    """

    wind = cycle(c == '>' for c in wind_data)
    rows = [FULL_ROW]
    shape_index = 0
    shape_count = 0
    repeats = []

    while shape_count < max_shapes:
        if find_repeat and shape_count > 0:
            if rows[first_filled_row(rows)] == FULL_ROW:
                repeats.append((shape_index, shape_count, height(rows)))

                if len(repeats) == 2:
                    return repeats

        shape = SHAPES[shape_index]
        shape_index = (shape_index + 1) % len(SHAPES)

        shape_y = first_filled_row(rows) + 4
        needed_rows = shape_y + len(shape) - len(rows)
        rows += [EMPTY_ROW] * needed_rows

        while not any(rows[shape_y + index] & shape_row for index, shape_row in enumerate(shape)):
            if next(wind):
                possible = [shape_row >> 1 for shape_row in shape]
            else:
                possible = [shape_row << 1 for shape_row in shape]

            if not any(rows[shape_y + index] & shape_row for index, shape_row in enumerate(possible)):
                shape = possible

            shape_y -= 1

        for index, shape_row in enumerate(shape):
            rows[shape_y + 1 + index] |= shape_row

        shape_count += 1

    return height(rows)


def height(rows):
    height_value = len(rows) - 1
    top = -1

    while rows[top] == EMPTY_ROW:
        height_value -= 1
        top -= 1

    return height_value


def part1(data):
    """
    >>> part1(read_input())
    3153
    """

    return drop_shapes(data, 2022)


def part2(data):
    """
    >>> part2(read_input())
    1553665689155
    """

    shapes = 1000000000000

    repeats = drop_shapes(data, 30000, True)
    ((start_shape, start_count, start_height), (repeat_shape, repeat_count, repeat_height)) = repeats

    if start_shape != repeat_shape:
        raise ValueError()

    repeat_length = repeat_count - start_count
    repeat_height = repeat_height - start_height

    shapes -= start_count
    repeats = shapes // repeat_length
    shapes = shapes % repeat_length
    extra = drop_shapes(data, start_count + shapes) - start_height

    return start_height + repeats * repeat_height + extra


def main():
    print(part1(read_input()))
    print(part2(read_input()))


if __name__ == "__main__":
    main()
