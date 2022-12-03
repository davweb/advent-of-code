# -*- coding: utf-8 -*-


def read_input():
    with open('input/2016/day12-input.txt', encoding='utf8') as file:
        return [line.strip().split() for line in file.readlines()]


def run(lines, a=0, b=0, c=0, d=0):
    register = { 'a': a, 'b': b, 'c': c, 'd': d }
    index = 0
    end = len(lines)

    while index < end:
        line = lines[index]
        instruction = line[0]
        x = line[1]
        y = None if len(line) < 3 else line[2]
        jump = 1

        match instruction, x, y:
            case 'cpy', 'a' | 'b' | 'c' | 'd' as source, dest:
                register[dest] = register[source]
            case 'cpy', value, dest:
                register[dest] = int(value)
            case 'inc', name, _:
                register[name] += 1
            case 'dec', name, _:
                register[name] -= 1
            case 'jnz', 'a' | 'b' | 'c' | 'd' as source, delta:
                if register[source] != 0:
                    jump = int(delta)
            case 'jnz', value, delta:
                if int(value) != 0:
                    jump = int(delta)
            case _:
                raise ValueError(line)

        index += jump

    return register


def part1(data):
    """
    >>> part1(read_input())
    318009
    """

    registers = run(data)
    return registers['a']


def part2(data):
    """
    >>> part2(read_input())
    9227663
    """

    registers = run(lines=data, c = 1)
    return registers['a']


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
