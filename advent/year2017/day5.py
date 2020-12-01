#!/usr/local/bin/python3

def read_input():
    file = open('input/2017/day5-input.txt', 'r')
    return [int(line) for line in file]


def part1(instructions):
    """
    >>> part1([0, 3, 0, 1, -3])
    5
    >>> part1(read_input())
    318883
    """
   
    size = len(instructions)
    index = 0
    count = 0

    while 0 <= index < size:
        jump = instructions[index]
        instructions[index] += 1
        index += jump
        count += 1

    return count


def part2(instructions):
    """
    >>> part2([0, 3, 0, 1, -3])
    10
    >>> part2(read_input())
    23948711
    """

    size = len(instructions)
    index = 0
    count = 0

    while 0 <= index < size:
        jump = instructions[index]

        if jump >= 3:
            instructions[index] = jump - 1
        else:
            instructions[index] = jump + 1

        index += jump
        count += 1

    return count


def main():
    print(part1(read_input()))
    print(part2(read_input()))


if __name__ == "__main__":
    main()
