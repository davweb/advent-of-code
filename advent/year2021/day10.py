# -*- coding: utf-8 -*-


CORRUPT_SCORE = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

REMAINING_SCORE = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
}


def read_input():
    with open("input/2021/day10-input.txt", "r") as file:
        return [line.strip() for line in file.readlines()]


def is_corrupt(line):
    """
    >>> is_corrupt('([])')
    (False, [])
    >>> is_corrupt('{()()()}')
    (False, [])
    >>> is_corrupt('<([{}])>')
    (False, [])
    >>> is_corrupt('[<>({}){}[([])<>]]')
    (False, [])
    >>> is_corrupt('(((((((((())))))))))')
    (False, [])
    >>> is_corrupt('{([(<{}[<>[]}>{[]{[(<()>')
    (True, '}')
    >>> is_corrupt('[[<[([]))<([[{}[[()]]]')
    (True, ')')
    >>> is_corrupt('[{[{({}]{}}([{[{{{}}([]')
    (True, ']')
    >>> is_corrupt('[<(<(<(<{}))><([]([]()')
    (True, ')')
    >>> is_corrupt('<{([([[(<>()){}]>(<<{{')
    (True, '>')
    >>> is_corrupt('[({(<(())[]>[[{[]{<()<>>')
    (False, ['}', '}', ']', ']', ')', '}', ')', ']'])
    >>> is_corrupt('[(()[<>])]({[<{<<[]>>(')
    (False, [')', '}', '>', ']', '}', ')'])
    >>> is_corrupt('(((({<>}<{<{<>}{[]{[]{}')
    (False, ['}', '}', '>', '}', '>', ')', ')', ')', ')'])
    """

    stack = []

    for char in line:
        if char == '(':
            stack.append(')')
        elif char == '[':
            stack.append(']')
        elif char == '{':
            stack.append('}')
        elif char == '<':
            stack.append('>')
        else:
            expected = stack.pop()

            if char != expected:
                return True, char

    stack.reverse()
    return False, stack


def corrupt_score(line):
    corrupt, char = is_corrupt(line)

    if not corrupt:
        return 0

    return CORRUPT_SCORE[char]


def remaining_score(line):
    """
    >>> remaining_score('(]')
    0
    >>> remaining_score('<{([')
    294
    """

    corrupt, remaining = is_corrupt(line)

    if corrupt:
        return 0

    score = 0

    for char in remaining:
        score = score * 5 + REMAINING_SCORE[char]

    return score


def part1(data):
    """
    >>> part1(read_input())
    193275
    """

    return sum(corrupt_score(line) for line in data)


def part2(data):
    """
    >>> part2(read_input())
    2429644557
    """

    scores = (remaining_score(line) for line in data)
    scores = sorted(score for score in scores if score != 0)
    return scores[len(scores) // 2]


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
