# pylint: disable=line-too-long
# -*- coding: utf-8 -*-

def read_input(filename='input/2022/day10-input.txt'):
    with open(filename, encoding='utf8') as file:
        return [line.strip() for line in file.readlines()]


def run_code(data):
    instructions = []

    for line in data:
        if line.startswith('addx '):
            instructions.append('noop')
        instructions.append(line)

    x = 1

    for line in instructions:
        yield x

        if line == "noop":
            pass
        elif line.startswith('addx '):
            x += int(line[5:])
        else:
            raise ValueError()


def signal_strength(data):
    """
    >>> signal_strength(read_input('input/2022/day10-test.txt'))
    13140
    """

    strength = 0

    for cycle, x in enumerate(run_code(data), start=1):
        if (cycle - 20) % 40 == 0:
            strength += cycle * x

    return strength


def part1(data):
    """
    >>> part1(read_input())
    13520
    """

    return signal_strength(data)


def part2(data):
    """
    >>> part2(read_input())
    '███   ██  ███  █  █ ███  ████  ██  ███  \\n█  █ █  █ █  █ █  █ █  █ █    █  █ █  █ \\n█  █ █    █  █ ████ ███  ███  █  █ ███  \\n███  █ ██ ███  █  █ █  █ █    ████ █  █ \\n█    █  █ █    █  █ █  █ █    █  █ █  █ \\n█     ███ █    █  █ ███  ████ █  █ ███  '
    """

    values = run_code(data)
    lines = []

    for _ in range(6):
        line = ''

        for x in range(40):
            value = next(values)
            line += '█' if value - 1 <= x <= value + 1 else ' '

        lines.append(line)

    return '\n'.join(lines)


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
