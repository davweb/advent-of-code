import re

ASCII_A = ord('a')
SPIN = re.compile(r"s(\d+)")
EXCHANGE = re.compile(r"x(\d+)/(\d+)")
PARTNER = re.compile(r"p([a-z])/([a-z])")
LINE_SIZE = 16


def read_input():
    file = open('input/2017/day16-input.txt', 'r')
    return parse_dance(file.read())


def parse_dance(dance):
    return [match(step) for step in dance.split(',')]


def match(line):
    spin = SPIN.match(line)
    if spin:
        return ('spin', int(spin.group(1)))

    exchange = EXCHANGE.match(line)
    if exchange:
        return ('exchange', [int(x) for x in exchange.group(1, 2)])

    partner = PARTNER.match(line)
    if partner:
        return ('partner', partner.group(1, 2))

    raise Exception("Did not match line '{}'".format(line))


def dance_move(line, step):
    line = list(line)
    move, details = step

    if move == 'spin':
        line = line[-details:] + line[:-details]
    elif move == 'exchange':
        a, b = details
        line[a], line[b] = line[b], line[a]
    elif move == 'partner':
        x, y = details
        a = line.index(x)
        b = line.index(y)
        line[a], line[b] = line[b], line[a]
    else:
        raise Exception("Did not match move '{}'".format(move))

    return "".join(line)


def create_line(line_size):
    """
    >>> create_line(16)
    'abcdefghijklmnop'
    """

    return "".join(chr(c) for c in range(ASCII_A, ASCII_A + line_size))


def do_dance(dance, line):
    """
    >>> line = create_line(5)
    >>> dance = parse_dance('s1,x3/4,pe/b')
    >>> do_dance(dance, line)
    'baedc'
    """

    for step in dance:
        line = dance_move(line, step)

    return line


def part1(dance):
    """
    >>> part1(read_input())
    'namdgkbhifpceloj'
    """

    line = create_line(LINE_SIZE)
    return do_dance(dance, line)


def part2(dance):
    """
    >>> part2(read_input())
    'ibmchklnofjpdeag'
    """

    line = create_line(LINE_SIZE)
    history = []

    while line not in history:
        history.append(line)
        line = do_dance(dance, line)

    return history[1000000000 % len(history)]


def main():
    dance = read_input()
    print(part1(dance))
    print(part2(dance))


if __name__ == "__main__":
    main()
