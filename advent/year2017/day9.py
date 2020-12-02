def read_input():
    file = open('input/2017/day9-input.txt', 'r')
    return file.read()


def part1and2(data):
    """
    >>> part1and2("{{<ab>},{<ab>},{<ab>},{<ab>}}")
    (9, 8)
    >>> part1and2("{{<!!>},{<!!>},{<!!>},{<!!>}}")
    (9, 0)
    >>> part1and2("{{<a!>},{<a!>},{<a!>},{<ab>}}")
    (3, 17)
    >>> part1and2(read_input())
    (14190, 7053)
    """

    score = 0
    depth = 0
    garbage = False
    garbage_count = 0
    ignore = False

    for char in data:
        if ignore:
            ignore = False
        elif char == '!':
            ignore = True
        elif garbage:
            if char == '>':
                garbage = False
            else:
                garbage_count += 1
        elif char == '<':
            garbage = True
        elif char == '{':
            depth += 1
        elif char == '}':
            score += depth
            depth -= 1

    return score, garbage_count


def main():
    data = read_input()
    print(part1and2(data))


if __name__ == "__main__":
    main()