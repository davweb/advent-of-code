# -*- coding: utf-8 -

import operator


def read_input():
    file = open('input/2020/day18-input.txt', 'r')
    return [[int(v) if v not in ('+', '*', '(', ')') else v for v in line.strip() if v != ' '] for line in file.readlines()]


def calculate(line):
    """
    >>> calculate([1, '+', 2, '*', 3, '+', 4, '*', 5, '+', 6])
    71
    >>> calculate([1, '+', '(', 2, '*', 3, ')', '+', '(', 4, '*', '(', 5, '+', 6, ')', ')'])
    51
    """
    
    stack = []
    group = 0
    op = operator.add

    for c in line:
        if c == '(':
            stack.append((group, op))
            group = 0
            op = operator.add
        elif c == ')':
            value = group
            group, op = stack.pop()
            group = op(group, value)
        elif c == '+':
            op = operator.add
        elif c == '*':
            op = operator.mul
        else:
            group = op(group, c)

    return group


def calculate_group(group):
    """
    >>> calculate_group([1, '+', 2, '*', 3, '+', 4, '*', 5, '+', 6])
    231
    """

    for(c, op) in (('+', operator.add), (('*'), operator.mul)):
        while c in group:
            i = group.index(c)
            group[i - 1:i + 2] = [op(group[i - 1], group[i + 1])]

    return group[0]


def brackets(line):
    """
    >>> brackets([1, '+', 2, '*', 3, '+', 4, '*', 5, '+', 6])
    231
    >>> brackets([1, '+', '(', 2, '*', 3, ')', '+', '(', 4, '*', '(', 5, '+', 6, ')', ')'])
    51
    """
    
    stack = []
    group = []

    for c in line:
        if c == '(':
            stack.append(group)
            group = []
        elif c == ')':
            value = calculate_group(group)
            group = stack.pop()
            group.append(value)
        else:
            group.append(c)

    return calculate_group(group)


def part1(data):
    """
    >>> part1(read_input())
    23507031841020
    """

    return sum(calculate(line) for line in data)


def part2(data):
    """
    >>> part2(read_input())
    218621700997826
    """
    
    return sum(brackets(line) for line in data)


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
