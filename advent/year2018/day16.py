import re
from collections import defaultdict

INSTRUCTION_PATTERN = re.compile(
    r"Before: \[(\d+), (\d+), (\d+), (\d+)\]\n"
    r"(\d+) (\d+) (\d+) (\d+)\n"
    r"After:  \[(\d+), (\d+), (\d+), (\d+)\]")


def read_input():
    file = open('input/2018/day16-input.txt', 'r')
    text = file.read()
    
    (samples, listing) = text.split("\n\n\n\n")

    instructions = []

    for groups in INSTRUCTION_PATTERN.findall(samples):
        values = [int(group) for group in groups]

        before_registers = values[0:4]
        instruction = values[4:8]
        after_registers = values[8:]

        instructions.append((before_registers, instruction, after_registers))

    code = []

    for line in listing.strip().split("\n"):
        instruction = [int(i) for i in line.strip().split(" ")]
        code.append(instruction)

    return (instructions, code)


def addr(registers, a, b, c):
    """
    addr (add register) stores into register C the result of adding register A and register B.

    >>> registers = [3, 2, 1, 0]
    >>> addr(registers, 0, 1, 2)
    >>> registers
    [3, 2, 5, 0]
    """
    
    registers[c] = registers[a] + registers[b]


def addi(registers, a, b, c):
    """
    addi (add immediate) stores into register C the result of adding register A and value B.

    >>> registers = [3, 2, 1, 0]
    >>> addi(registers, 0, 1, 2)
    >>> registers
    [3, 2, 4, 0]
    """

    registers[c] = registers[a] + b


def mulr(registers, a, b, c):
    """
    mulr (multiply register) stores into register C the result of multiplying register A and register B.

    >>> registers = [3, 2, 1, 1]
    >>> mulr(registers, 2, 1, 2)
    >>> registers
    [3, 2, 2, 1]
    """

    registers[c] = registers[a] * registers[b]


def muli(registers, a, b, c):
    """
    muli (multiply immediate) stores into register C the result of multiplying register A and value B.

    >>> registers = [3, 2, 1, 0]
    >>> muli(registers, 0, 1, 2)
    >>> registers
    [3, 2, 3, 0]
    """

    registers[c] = registers[a] * b


def banr(registers, a, b, c):
    """
    banr (bitwise AND register) stores into register C the result of the bitwise AND of register A and register B.

    >>> registers = [3, 2, 1, 0]
    >>> banr(registers, 0, 1, 2)
    >>> registers
    [3, 2, 2, 0]
    """

    registers[c] = registers[a] & registers[b]


def bani(registers, a, b, c):
    """
    bani (bitwise AND immediate) stores into register C the result of the bitwise AND of register A and value B.

    >>> registers = [3, 2, 1, 0]
    >>> bani(registers, 0, 1, 2)
    >>> registers
    [3, 2, 1, 0]
    """

    registers[c] = registers[a] & b


def borr(registers, a, b, c):
    """
    borr (bitwise OR register) stores into register C the result of the bitwise OR of register A and register B.

    >>> registers = [3, 2, 1, 0]
    >>> borr(registers, 0, 1, 2)
    >>> registers
    [3, 2, 3, 0]
    """

    registers[c] = registers[a] | registers[b]


def bori(registers, a, b, c):
    """
    bori (bitwise OR immediate) stores into register C the result of the bitwise OR of register A and value B.

    >>> registers = [3, 2, 1, 0]
    >>> bori(registers, 0, 1, 2)
    >>> registers
    [3, 2, 3, 0]
    """

    registers[c] = registers[a] | b


def setr(registers, a, b, c):
    """
    setr (set register) copies the contents of register A into register C. (Input B is ignored.)

    >>> registers = [3, 2, 1, 0]
    >>> setr(registers, 0, 1, 2)
    >>> registers
    [3, 2, 3, 0]
    """

    registers[c] = registers[a] 


def seti(registers, a, b, c):
    """
    seti (set immediate) stores value A into register C. (Input B is ignored.)

    >>> registers = [3, 2, 1, 0]
    >>> seti(registers, 0, 1, 2)
    >>> registers
    [3, 2, 0, 0]
    """

    registers[c] = a


def gtir(registers, a, b, c):
    """
    gtir (greater-than immediate/register) sets register C to 1 if value A is greater than register B. Otherwise, register C is set to 0.

    >>> registers = [3, 2, 2, 0]
    >>> gtir(registers, 0, 1, 2)
    >>> registers
    [3, 2, 0, 0]
    """

    registers[c] = 1 if a > registers[b] else 0


def gtri(registers, a, b, c):
    """
    gtri (greater-than register/immediate) sets register C to 1 if register A is greater than value B. Otherwise, register C is set to 0.

    >>> registers = [3, 2, 2, 0]
    >>> gtri(registers, 0, 1, 2)
    >>> registers
    [3, 2, 1, 0]
    """

    registers[c] = 1 if registers[a] > b else 0


def gtrr(registers, a, b, c):
    """
    gtrr (greater-than register/register) sets register C to 1 if register A is greater than register B. Otherwise, register C is set to 0.

    >>> registers = [3, 2, 2, 0]
    >>> gtrr(registers, 0, 1, 2)
    >>> registers
    [3, 2, 1, 0]
    """

    registers[c] = 1 if registers[a] > registers[b] else 0

def eqir(registers, a, b, c):
    """
    eqir (equal immediate/register) sets register C to 1 if value A is equal to register B. Otherwise, register C is set to 0.

    >>> registers = [3, 2, 2, 0]
    >>> eqir(registers, 0, 1, 2)
    >>> registers
    [3, 2, 0, 0]
    """

    registers[c] = 1 if a == registers[b] else 0


def eqri(registers, a, b, c):
    """
    eqri (equal register/immediate) sets register C to 1 if register A is equal to value B. Otherwise, register C is set to 0.

    >>> registers = [3, 2, 2, 0]
    >>> eqri(registers, 0, 1, 2)
    >>> registers
    [3, 2, 0, 0]
    """

    registers[c] = 1 if registers[a] == b else 0


def eqrr(registers, a, b, c):
    """
    eqrr (equal register/register) sets register C to 1 if register A is equal to register B. Otherwise, register C is set to 0.

    >>> registers = [3, 2, 2, 0]
    >>> eqrr(registers, 0, 1, 2)
    >>> registers
    [3, 2, 0, 0]
    """

    registers[c] = 1 if registers[a] == registers[b] else 0


def op_matches(before, after, a, b, c):
    """
    >>> len(op_matches([3, 2, 1, 1], [3, 2, 2, 1], 2, 1, 2))
    3
    """
    
    ops = [addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr]
    matches = []

    for op in ops:
        copy = list(before)
        op(copy, a, b, c)

        if copy == after:
            matches.append(op)

    return matches


def part1(data):
    """
    >>> part1(read_input())
    529
    """

    count = 0

    for (before, instruction, after) in data[0]:
        (_, a, b, c) = instruction
        
        if len(op_matches(before, after, a, b, c)) >= 3:
            count += 1
    
    return count


def part2(data):
    """
    >>> part2(read_input())
    573
    """

    samples, code = data
    match_map = defaultdict(set)

    for (before, instruction, after) in samples:
        (op_id, a, b, c) = instruction
        matches = op_matches(before, after, a, b, c)

        for match in matches:
            match_map[op_id].add(match)

    op_map = {}

    while sum(len(matches) for matches in match_map.values()) > 0:
        # Find the first id that maps to only one function
        op_id, op = next(iter((key, next(iter(matches))) for key, matches in match_map.items() if len(matches) == 1))
        
        # record the mapping found
        op_map[op_id] = op

        # exclude that operation from all the other lists
        for matches in match_map.values():
            if op in matches:
                matches.remove(op)

    registers = [0, 0, 0, 0]

    for instruction in code:
        op_id, a, b, c = instruction
        op_map[op_id](registers, a, b, c)

    return registers[0]


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
