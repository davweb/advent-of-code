#!/usr/local/bin/python3

import functools


def read_input():
    with open('input/2019/day16-input.txt', encoding='utf-8') as file:
        return file.read()

# def pattern(element_no):
#     """
#     >>> list(itertools.islice(pattern(0), 8))
#     [1, 0, -1, 0, 1, 0, -1, 0]
#     >>> list(itertools.islice(pattern(1), 8))
#     [0, 1, 1, 0, 0, -1, -1, 0]
#     >>> list(itertools.islice(pattern(2), 10))
#     [0, 0, 1, 1, 1, 0, 0, 0, -1, -1]
#     """

#     first = True

#     while True:
#         for i in [0, 1, 0, -1]:
#             for _ in range(0, element_no  + 1):
#                 if first:
#                     first = False
#                 else:
#                     yield i

# def transform(input):
#     output = []

#     for i in range(0, len(input)):
#         output.append(abs(sum((a * b) for (a, b) in zip(input, pattern(i)))) % 10)

#     return output


def pattern_series(element_no, size):
    """
    >>> list(pattern_series(0, 8))
    [(1, 0, 1), (-1, 2, 3), (1, 4, 5), (-1, 6, 7)]
    >>> list(pattern_series(2, 10))
    [(1, 2, 5), (-1, 8, 10)]
    >>> list(pattern_series(48, 50))
    [(1, 48, 50)]
    """

    length = element_no + 1
    modifier = 1
    start = element_no

    while start < size:
        end = min(start + length, size)
        yield (modifier, start, end)
        start += 2 * length
        modifier = - modifier


def transform(input_value):
    output = []
    length = len(input_value)

    for i in range(0, length):
        value = sum(modifier * sum(input_value[start:end]) for (modifier, start, end) in pattern_series(i, length))
        output.append(abs(value) % 10)

    return output


def sum_input(input_value, start, end, cache):
    if start == end:
        return 0

    if end - start == 1:
        return input_value[start]

    key = (start, end)

    try:
        return cache[key]
    except KeyError:
        middle = start + (end - start) // 2
        value = sum_input(input_value, start, middle, cache) + sum_input(input_value, middle, end, cache)
        cache[key] = value
        return value


def transform_cache(input_value):
    print(".")
    output = []
    length = len(input_value)
    cache = {}

    for i in range(0, length):
        value = 0

        for (modifier, start, end) in pattern_series(i, length):
            value += modifier * sum_input(input_value, start, end, cache)

        output.append(abs(value) % 10)

    return output


def fft(input_value):
    """
    >>> fft('12345678')
    '48226158'
    >>> fft('48226158')
    '34040438'
    >>> fft('34040438')
    '03415518'
    >>> fft('03415518')
    '01029498'
    """

    input_value = [int(code) for code in input_value]
    output = transform(input_value)
    return "".join(str(i) for i in output)


def part1(data):
    """
    >>> part1('80871224585914546619083218645595')
    '24176176'

    >>> part1(read_input())
    '15841929'
    """
    data = [int(code) for code in data]
    output = functools.reduce(lambda a, b: transform(a), [data] + list(range(0, 100)))
    return "".join(str(i) for i in output[:8])


def part2(data):
    """
    # >>> part2('80871224585914546619083218645595')
    '24176176'

    # >>> part2(read_input())
    '15841929'
    """

    data = [int(code) for code in data]
    output = functools.reduce(lambda a, b: transform_cache(a), [data] + list(range(0, 100)))
    return "".join(str(i) for i in output[:8])


def main():
    data = read_input()
    print(len(data))
    print(part1(data))
    print(part2(data * 100))


if __name__ == "__main__":
    main()
