# -*- coding: utf-8 -*-


def read_input():
    output = []
    with open('input/2016/day20-input.txt', encoding='utf8') as file:
        for line in file.readlines():
            (lower, upper) = line.strip().split('-')
            output.append((int(lower), int(upper)))

    return output


class Range():
    def __init__(self, lower, upper):
        if lower >= upper:
            raise ValueError

        self.lower = lower
        self.upper = upper

    def size(self):
        return self.upper - self.lower + 1

    def overlaps(self, other):
        return self.lower <= other.lower <= self.upper \
            or self.lower <= other.upper <= self.upper

    def merge(self, other):
        self.lower = min(self.lower, other.lower)
        self.upper = max(self.upper, other.upper)

    def __lt__(self, other):
        if self.lower == other.lower:
            return self.upper < other.upper
        else:
            return self.lower < other.lower

    def __repr__(self):
        return f'Range({self.lower}, {self.upper})'


def part1(data):
    """
    >>> part1(read_input())
    14975795
    """

    minimum = 0

    for lower, upper in sorted(data):
        if lower <= minimum <= upper:
            minimum = upper + 1

    return minimum


def part2(data):
    """
    >>> part2(read_input())
    101
    """

    ranges = sorted(Range(lower, upper) for lower, upper in data)

    lower_range = ranges.pop(0)
    merged = [lower_range]

    while ranges:
        upper_range = ranges.pop(0)

        if lower_range.overlaps(upper_range):
            lower_range.merge(upper_range)
        else:
            lower_range = upper_range
            merged.append(lower_range)

    return 4294967296 - sum(range.size() for range in merged)


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
