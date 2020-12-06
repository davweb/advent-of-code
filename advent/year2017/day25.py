import re

INITIAL_STATE_PATTERN = re.compile(r"Begin in state ([A-Z]).")
CHECKSUM_PATTERN = re.compile(r"Perform a diagnostic checksum after (\d+) steps.")
STATE_PATTERN = re.compile(
    r"In state ([A-Z]):\n"
    r"  If the current value is 0:\n"
    r"    - Write the value (\d).\n"
    r"    - Move one slot to the (left|right).\n"
    r"    - Continue with state ([A-Z]).\n"
    r"  If the current value is 1:\n"
    r"    - Write the value (\d).\n"
    r"    - Move one slot to the (left|right).\n"
    r"    - Continue with state ([A-Z]).\n")


def read_input():
    file = open('input/2017/day25-input.txt', 'r')
    contents = file.read()

    match = INITIAL_STATE_PATTERN.search(contents)
    initial_state = match.group(1)

    match = CHECKSUM_PATTERN.search(contents)
    checksum_steps = int(match.group(1))

    rules = {}

    for groups in STATE_PATTERN.findall(contents):
        state = groups[0]
        zero_value = int(groups[1])
        zero_move = -1 if groups[2] == 'left' else 1
        zero_state = groups[3]
        one_value = int(groups[4])
        one_move = -1 if groups[5] == 'left' else 1
        one_state = groups[6]

        rules[(state, 0)] = (zero_value, zero_move, zero_state)
        rules[(state, 1)] = (one_value, one_move, one_state)

    return (initial_state, checksum_steps, rules)


def part1(data):
    """
    >>> part1(('A', 6, { 
    ...    ('A', 0): (1, 1, 'B'), 
    ...    ('A', 1): (0, -1, 'B'),
    ...    ('B', 0): (1, -1, 'A'),
    ...    ('B', 1): (1, 1, 'A')
    ... }))
    3
    >>> part1(read_input())
    3145
    """

    state, max_steps, rules = data

    tape = {}
    cursor = 0
    step = 0

    while step < max_steps:
        step += 1
        current = tape.get(cursor, 0)
        tape[cursor], move, state = rules[(state, current)]
        cursor += move

    return sum(tape.values())


def main():
    data = read_input();
    print(part1(data))


if __name__ == "__main__":
    main()
