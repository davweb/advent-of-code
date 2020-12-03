def split_rule(rule):
    """
    >>> split_rule('AB/CD')
    [['A', 'B'], ['C', 'D']]
    """
    
    return [list(row) for row in rule.split('/')]


def join_rule(value):
    """
    >>> join_rule([['A', 'B'], ['C', 'D']])
    'AB/CD'
    """

    return "/".join("".join(row) for row in value)


def rotations(rule):
    """
    >>> sorted(rotations("ABC/DEF/GHI"))    
    ['ABC/DEF/GHI', 'CFI/BEH/ADG', 'GDA/HEB/IFC', 'IHG/FED/CBA']
    >>> sorted(rotations("AB/CD"))    
    ['AB/CD', 'BD/AC', 'CA/DB', 'DC/BA']
    """
    
    value = split_rule(rule)
    rotations = []

    for _ in range(4):
        rotations.append(value)
        value = list(zip(*value[::-1]))

    return (join_rule(rotation) for rotation in rotations) 


def flips(rule):
    """
    >>> sorted(flips("AB/CD"))    
    ['AB/CD', 'BA/DC', 'CD/AB']
    >>> sorted(flips("ABC/DEF/GHI"))
    ['ABC/DEF/GHI', 'CBA/FED/IHG', 'GHI/DEF/ABC']
    """
    
    value = split_rule(rule)
    
    flips = []
    flips.append(value)
    flips.append(reversed(value))
    flips.append(reversed(row) for row in value)

    return (join_rule(flip) for flip in flips)


def permutations(rule):
    """
    >>> sorted(permutations("AB/CD"))    
    ['AB/CD', 'AC/BD', 'BA/DC', 'BD/AC', 'CA/DB', 'CD/AB', 'DB/CA', 'DC/BA']
    """
    
    result = set()

    for rotation in rotations(rule):
        for flip in flips(rotation):
            result.add(flip)

    return result


def read_input():
    rules = {}

    for line in open('input/2017/day21-input.txt', 'r'):
        (rule, result) = line.strip().split(' => ')

        for permutation in permutations(rule):
            rules[permutation] = result

    return rules


def process(rules, steps):
    pattern = ".#.\n..#\n###" 
    step = 0

    # Break the pattern into blocks
    while step < steps:
        step += 1
        lines = pattern.split()

        if len(lines) % 2 == 0:
            size = 2
            output_size = 3
        else:
            size = 3
            output_size = 4

        keys = []

        for i in range(0, len(lines), size):
            row = []

            for j in range(0, len(lines), size):
                key = []
                
                for k in range(0, size):
                    key.append(lines[i + k][j:j + size])

                row.append("/".join(key))

            keys.append(row)

        output = [[rules[key] for key in row] for row in keys]

        # Transform with the rules
        new_pattern = []

        # Rebuild the pattern
        for row in output:
            lines = ['' for _ in range(0, output_size)]

            for block in row:
                block = block.split('/')
                for j in range(0, output_size):
                    lines[j] += block[j]

            new_pattern.extend(lines)

        pattern = '\n'.join(new_pattern)

    return pattern.count('#')


def part1(rules):
    """
    >>> part1(read_input())
    205
    """

    return process(rules, 5)


def part2(rules):
    """
    >>> part2(read_input())
    3389823
    """
    
    return process(rules, 18)


def main():
    rules = read_input();
    print(part1(rules))
    print(part2(rules))


if __name__ == "__main__":
    main()

