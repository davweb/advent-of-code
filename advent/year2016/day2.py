# -*- coding: utf-8 -*-

def read_input():
    with open('input/2016/day2-input.txt', encoding='utf8') as file:
        return [line.strip() for line in file.readlines()]


def make_move(digit, move):
    """
    >>> make_move(4, 'U')
    '1'
    >>> make_move(2, 'U')
    '2'
    >>> make_move(2, 'D')
    '5'
    >>> make_move(2, 'L')
    '1'
    >>> make_move(2, 'R')
    '3'
    >>> make_move(3, 'R')
    '3'
    """

    digit = int(digit)

    if move == 'U':
        if digit > 3:
            digit -= 3
    elif move == 'D':
        if digit < 7:
            digit += 3
    elif move == 'L':
        if digit not in (1, 4, 7):
            digit -= 1
    elif move == 'R':
        if digit not in (3, 6, 9):
            digit += 1
    else:
        raise ValueError(f'Unrecognised move "{move}"')

    return str(digit)


def make_other_move(digit, move):
    """
    >>> make_other_move('4', 'U')
    '4'
    >>> make_other_move('2', 'U')
    '2'
    >>> make_other_move('2', 'D')
    '6'
    >>> make_other_move('2', 'L')
    '2'
    >>> make_other_move('2', 'R')
    '3'
    >>> make_other_move('3', 'R')
    '4'
    """

    moves = {
        '1': [None, '3', None, None],
        '2': [None, '6', None, '3'],
        '3': ['1', '7', '2', '4'],
        '4': [None, '8', '3', None],
        '5': [None, None, None, '6'],
        '6': ['2', 'A', '5', '7'],
        '7': ['3', 'B', '6', '8'],
        '8': ['4', 'C', '7', '9'],
        '9': [None, None, '8', None],
        'A': ['6', None, None, 'B'],
        'B': ['7', 'D', 'A', 'C'],
        'C': ['8', None, 'B', None],
        'D': ['B', None, None, None]
    }

    index = 'UDLR'.index(move)
    next_digit = moves[digit][index]
    return digit if next_digit is None else next_digit


def process(data, move_function):
    code = ''
    digit = '5'

    for line in data:
        for move in line:
            digit = move_function(digit, move)

        code += digit

    return code


def part1(data):
    """
    >>> part1(read_input())
    '38961'
    """

    return process(data, make_move)


def part2(data):
    """
    >>> part2(read_input())
    '46C92'
    """

    return process(data, make_other_move)


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
