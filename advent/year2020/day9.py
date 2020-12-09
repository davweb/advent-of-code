from os import truncate
import re
from itertools import combinations

def read_input():
    file = open('input/2020/day9-input.txt', 'r')
    return [int(line.strip()) for line in file.readlines()]


def validate_stream(window, stream):
    """
    >>> validate_stream(5, [35, 20, 15, 25, 47, 40, 62, 55, 65, 95, 102, 117, 150, 182, 127, 219, 299, 277, 309, 576])
    127
    """

    previous = stream[0:window]
    del(stream[0:window])

    for number in stream:
        valid_numbers = [sum(x) for x in combinations(previous, 2)]

        if number not in valid_numbers:
            return number
    
        previous.pop(0)
        previous.append(number)

    raise ValueError("Whole stream is valid")


def find_combination(value, stream):
    """
    >>> find_combination(127, [35, 20, 15, 25, 47, 40, 62, 55, 65, 95, 102, 117, 150, 182, 127, 219, 299, 277, 309, 576])
    62
    """

    x = 0
    y = 2

    while True:
        total = sum(stream[x:y])

        if total < value:
            y += 1
        elif total > value:
            x += 1
        else:
            return min(stream[x:y]) + max(stream[x:y])


def part1(data):
    """
    >>> part1(read_input())
    26134589
    """
 
    return validate_stream(25, data)


def part2(data):
    """
    >>> part2(read_input())
    3535124
    """

    value = validate_stream(25, data)
    return find_combination(value, data)


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
