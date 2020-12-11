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
