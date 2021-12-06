# -*- coding: utf-8 -*-

import string

INPUT = 'cqjxjnds'


def valid_password(password):
    """
    >>> valid_password('hijklmmn')
    False
    >>> valid_password('abbceffg')
    False
    >>> valid_password('abbcegjk')
    False
    >>> valid_password('abcdffaa')
    True
    >>> valid_password('ghjaabcc')
    True
    """

    if 'i' in password or 'o' in password or 'l' in password:
        return False

    count_pairs = sum((c * 2) in password for c in string.ascii_lowercase)

    if count_pairs < 2:
        return False

    for i in range(0, len(password) - 2):
        if ord(password[i]) == ord(password[i + 1]) - 1 == ord(password[i + 2]) - 2:
            return True

    return False


def increment_password(password):
    """
    >>> increment_password('aa')
    'ab'
    >>> increment_password('az')
    'ba'
    >>> increment_password('buzz')
    'bvaa'
    """

    last_char = password[-1]
    remainder = password[:-1]

    if last_char == 'z':
        return increment_password(remainder) + 'a'
    else:
        return remainder + chr(ord(last_char) + 1)


def next_password(password):
    password = increment_password(password)

    while not valid_password(password):
        password = increment_password(password)

    return password


def part1(data):
    """
    >>> part1(INPUT)
    'cqjxxyzz'
    """

    return next_password(data)


def part2(data):
    """
    >>> part2(INPUT)
    'cqkaabcc'
    """

    return next_password(next_password(data))


def main():
    print(part1(INPUT))
    print(part2(INPUT))


if __name__ == "__main__":
    main()
