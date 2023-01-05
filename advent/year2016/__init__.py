# pylint: disable=used-before-assignment,too-many-locals,line-too-long

def value_of(value, register):
    if value in register:
        return register[value]
    return int(value)


def detect_multiply(lines, index, register):
    """
    >>> lines = [['cpy', 7, 'c'], ['inc', 'a'], ['dec', 'c'], ['jnz', 'c', '-2'], ['dec', 'd'], ['jnz', 'd', '-5'], ['cpy', 7, 'c']]
    >>> register = {'a': 5, 'b': 0, 'c': 0, 'd': 11}
    >>> detect_multiply(lines, 6, register)
    False
    >>> detect_multiply(lines, 0, register)
    True
    >>> register
    {'a': 82, 'b': 0, 'c': 0, 'd': 0}
    """

    match lines[index + 4:index + 6]:
        case [('inc' | 'dec') as op, first], ['jnz', second, '-5'] if first == second:
            var_right = first
            right = value_of(var_right, register)

            if op == 'dec':
                right = -right
        case _:
            return False

    match lines[index + 1:index + 4]:
        case [('inc' | 'dec') as first_op, first], [('inc' | 'dec') as second_op, second], ['jnz', third, '-2'] if first == third:
            var_counter = first
            var_dest = second

            if first_op != second_op:
                right = -right
        case [('inc' | 'dec') as first_op, first], [('inc' | 'dec') as second_op, second], ['jnz', third, '-2'] if second == third:
            var_dest = first
            var_counter = second

            if first_op != second_op:
                right = -right
        case _:
            return False

    match lines[index]:
        case['cpy', source, dest] if dest == var_counter:
            left = value_of(source, register)
        case _:
            return False

    register[var_counter] = 0
    register[var_right] = 0
    register[var_dest] += left * right

    return True


def run_assembunny(lines, a=0, c=0):
    """
    >>> run_assembunny([['cpy', 2, 'a'], ['tgl', 'a',], ['tgl', 'a',], ['tgl', 'a',], ['cpy', 1, 'a'], ['dec', 'a',], ['dec', 'a',]])
    3
    >>> run_assembunny([['cpy', '5', 'a'], ['cpy', '11', 'd'], ['cpy', 7, 'c'], ['inc', 'a'], ['dec', 'c'], ['jnz', 'c', '-2'], ['dec', 'd'], ['jnz', 'd', '-5']])
    82
    """

    output = []
    register = {'a': a, 'b': 0, 'c': c, 'd': 0}

    index = 0
    end = len(lines)

    while index < end and len(output) < 10:
        if detect_multiply(lines, index, register):
            index += 6
            continue

        line = lines[index]
        instruction = line[0]
        x = line[1]
        y = None if len(line) < 3 else line[2]

        jump = 1

        match instruction, x, y:
            case 'cpy', source, 'a' | 'b' | 'c' | 'd' as dest:
                register[dest] = value_of(source, register)
            case 'inc', name, _:
                register[name] += 1
            case 'dec', name, _:
                register[name] -= 1
            case 'jnz', source, delta:
                if value_of(source, register) != 0:
                    jump = value_of(delta, register)
            case 'tgl', name, _:
                change_index = index + register[name]

                if change_index < len(lines):
                    change_line = lines[change_index]

                    match change_line[0]:
                        case 'inc':
                            change_instruction = 'dec'
                        case 'dec' | 'tgl':
                            change_instruction = 'inc'
                        case 'jnz':
                            change_instruction = 'cpy'
                        case 'cpy':
                            change_instruction = 'jnz'
                        case _:
                            raise ValueError(change_line)

                    change_line[0] = change_instruction
            case 'out', name, _:
                output.append(register[name])
            case _:
                raise ValueError(line)

        index += jump

    return output if output else register['a']
