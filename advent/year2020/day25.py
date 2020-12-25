# -*- coding: utf-8 -*-

INPUT = (2959251, 4542595)


def calculate_loop_size(public_key):
    """
    >>> calculate_loop_size(5764801)
    8
    >>> calculate_loop_size(17807724)
    11
    """

    subject_number = 7
    value = 1
    loop_size = 0

    while value != public_key:
        value *= subject_number
        value %= 20201227
        loop_size += 1

    return loop_size


def transform(subject_number, loop_size):
    """
    >>> transform(17807724, 8)
    14897079
    >>> transform(5764801, 11)
    14897079
    """

    value = 1
    loop = 0

    while loop < loop_size:
        value *= subject_number
        value %= 20201227
        loop += 1

    return value


def part1(data):
    """
    >>> part1((5764801, 17807724))
    14897079
    >>> part1(INPUT)
    0
    """

    door_public_key, card_public_key = data

    door_loop_size = calculate_loop_size(door_public_key)
    card_loop_size = calculate_loop_size(card_public_key)

    door_key = transform(card_public_key, door_loop_size)
    card_key = transform(door_public_key, card_loop_size)

    if door_key != card_key:
        raise ValueError()

    return door_key


def main():
    print(part1(INPUT))


if __name__ == "__main__":
    main()
