# -*- coding: utf-8 -*-

def read_input():
    monkeys = {}

    with open('input/2022/day21-input.txt', encoding='utf8') as file:
        for line in file:
            monkey, value = line.strip().split(': ')
            monkeys[monkey] = value

    return monkeys


def arithmetic(left, op, right):
    match op:
        case '+':
            return left + right
        case '-':
            return left - right
        case '*':
            return left * right
        case '/':
            return left // right
        case _:
            raise ValueError(op)


def monkey_function(monkey, data):
    value = data[monkey]

    try:
        return int(value)
    except ValueError:
        pass

    if value == '?':
        return value

    left, op, right = value.split(' ')

    left = monkey_function(left, data)
    right = monkey_function(right, data)

    if not isinstance(left, int) or not isinstance(right, int):
        return (left, op, right)

    return arithmetic(left, op, right)


def part1(data):
    """
    >>> part1(read_input())
    194501589693264
    """

    return monkey_function('root', data)


def part2(data):
    """
    >>> part2(read_input())
    3887609741189
    """

    UNKNOWN = '?'

    left, _, right = data['root'].split(' ')
    data['humn'] = UNKNOWN

    left = monkey_function(left, data)
    right = monkey_function(right, data)

    if isinstance(left, int):
        number, expression = left, right
    else:
        number, expression = right, left

    while expression != UNKNOWN:
        left, op, right = expression

        match isinstance(left, int), op:
            case True, '+':
                number -= left
                expression = right
            case False, '+':
                number -= right
                expression = left
            case True, '-':
                number = left - number
                expression = right
            case False, '-':
                number = number + right
                expression = left
            case True, '*':
                number = number // left
                expression = right
            case False, '*':
                number = number // right
                expression = left
            case True, '/':
                number = left // number
                expression = right
            case False, '/':
                number = number * right
                expression = left

    return number


def main():
    print(part1(read_input()))
    print(part2(read_input()))


if __name__ == "__main__":
    main()
