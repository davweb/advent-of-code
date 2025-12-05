# -*- coding: utf-8 -*-

from advent import Span


def read_input(filename='input/2025/day5-input.txt'):
    spans = set()
    product_ids = []

    with open(filename, encoding='utf8') as file:
        for line in file.readlines():
            if '-' in line:
                start, end = line.split("-")
                spans.add(Span(int(start), int(end)))
            elif line.strip() != "":
                product_ids.append(int(line))

    return Span.combine(spans), product_ids


def part1(data):
    """
    >>> part1(read_input())
    520
    """

    spans, product_ids = data
    return sum(any(product_id in span for span in spans) for product_id in product_ids)


def part2(data):
    """
    >>> part2(read_input())
    347338785050515
    """

    spans, _ = data
    return sum(len(span) for span in spans)


def main():
    print(part1(read_input()))
    print(part2(read_input()))


if __name__ == "__main__":
    main()
