# -*- coding: utf-8 -*-

from collections import defaultdict, Counter


NUMBERS = {
    'abcefg': 0,
    'cf': 1,
    'acdeg': 2,
    'acdfg': 3,
    'bcdf': 4,
    'abdfg': 5,
    'abdefg': 6,
    'acf': 7,
    'abcdefg': 8,
    'abcdfg': 9
}


def read_input():
    data = []

    with open("input/2021/day8-input.txt", "r") as file:
        for line in file.readlines():
            inputs, outputs = line.split(' | ')
            data.append((inputs.split(), outputs.split()))

    return data


def calculate_total(inputs, outputs):
    """
    >>> calculate_total(
    ...     ('acedgfb', 'cdfbe', 'gcdfa', 'fbcad', 'dab', 'cefabd', 'cdfgeb', 'eafb', 'cagedb', 'ab'),
    ...     ('cdfeb', 'fcadb', 'cdfeb', 'cdbaf')
    ... )
    5353
    """

    mapping = get_mapping(inputs)
    reverse = {v: k for k, v in mapping.items()}

    result = 0
    unit = 1

    for output in outputs[::-1]:
        digit = "".join(sorted(reverse[c] for c in output))
        number = NUMBERS[digit]
        result += number * unit
        unit *= 10

    return result


def get_mapping(inputs):
    """
    >>> mapping = get_mapping(('acedgfb', 'cdfbe', 'gcdfa', 'fbcad', 'dab', 'cefabd', 'cdfgeb', 'eafb', 'cagedb', 'ab'))
    >>> sorted(mapping.items())
    [('a', 'd'), ('b', 'e'), ('c', 'a'), ('d', 'f'), ('e', 'g'), ('f', 'b'), ('g', 'c')]
    """

    # map of input length to input
    by_length = defaultdict(list)
    counter = Counter()

    for input_value in inputs:
        by_length[len(input_value)].append(input_value)
        counter.update(input_value)

    # map of count to letter in input
    by_count = defaultdict(list)

    for letter, count in counter.items():
        by_count[count].append(letter)

    # map of correct letter to input letter
    answer = {}

    # get segments by how often they appear in all numbers
    answer['b'] = by_count[6][0]
    answer['e'] = by_count[4][0]
    answer['f'] = by_count[9][0]

    # 1 has length 2 and is made up of c and f
    answer['c'] = by_length[2][0].replace(answer['f'], '')

    # 7 has length 3 abd is made up of a, c and, f
    answer['a'] = by_length[3][0].replace(answer['c'], '').replace(answer['f'], '')

    # d is the difference between 8 and 0 and we can work out 0 and just find 8 by length
    zero = [n for n in by_length[6] if answer['e'] in n and answer['c'] in n][0]
    answer['d'] = (set(by_length[7][0]) - set(zero)).pop()

    # g is what's left
    answer['g'] = (set('abcdefg') - set(answer.values())).pop()

    return answer


def part1(data):
    """
    >>> part1(read_input())
    554
    """

    count = 0

    for _, output in data:
        count += sum(1 for digit in output if len(digit) in (2, 3, 4, 7))

    return count


def part2(data):
    """
    >>> part2(read_input())
    990964
    """

    return sum(calculate_total(inputs, outputs) for inputs, outputs in data)


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
