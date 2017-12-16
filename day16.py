import re

ASCII_A = ord('a')
SPIN = re.compile(r"s(\d+)")
EXCHANGE = re.compile(r"x(\d+)/(\d+)")
PARTNER = re.compile(r"p([a-z])/([a-z])")

def read_input():
    return file('day16-input.txt').read().split(',')

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
    return "".join(chr(c) for c in range(ASCII_A, ASCII_A + line_size))

def do_dance(dance, line):
    for step in dance:
        line = dance_move(line, step)

    return line

def parse_dance(dance):
    return [match(step) for step in dance]

def part1(dance, line_size):
    line = create_line(line_size)
    dance = parse_dance(dance)
    print do_dance(dance, line)

def part2(dance, line_size):
    line = create_line(line_size)
    dance = parse_dance(dance)
    history = []

    while line not in history:
        history.append(line)
        line = do_dance(dance, line)

    print history[1000000000 % len(history)]

def main():
    part1('s1,x3/4,pe/b'.split(','), 5)
    dance = read_input()
    part1(dance, 16)
    part2(dance, 16)

if __name__ == "__main__":
    main()
