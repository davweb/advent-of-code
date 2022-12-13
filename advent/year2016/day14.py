# -*- coding: utf-8 -*-

import itertools
import re
from advent import md5


SALT = 'zpqevtbw'
FIVE_PATTERN = re.compile(r'(\w)\1\1\1\1')
THREE_PATTERN = re.compile(r'(\w)\1\1')


def repeats_five(haystack, needle):
    """
    >>> repeats_five('abbbbba', 'b')
    True
    >>> repeats_five('abbbbba', 'a')
    False
    """

    return needle * 5 in haystack


def repeats_three(haystack):
    """
    >>> repeats_three('abbbbba')
    'b'
    >>> repeats_three('abba')
    """

    match = THREE_PATTERN.search(haystack)
    return match.group(1) if match else None


def hashes(salt):
    """
    >>> h = hashes('abc')
    >>> x = None
    >>> for _ in range(19):
    ...     x = next(h)
    >>> x
    (18, '0034e0923cc38887a57bd7b1d4f953df')
    """

    i = 0

    while True:
        yield (i, md5(f'{salt}{i}'))
        i += 1


def stretched_hashes(salt):
    """
    >>> next(stretched_hashes('abc'))
    (0, 'a107ff634856bb300138cac6568c0f24')
    """

    i = 0

    while True:
        hash_value = md5(f'{salt}{i}')

        for _ in range(2016):
            hash_value = md5(hash_value)

        yield (i, hash_value)
        i += 1


def pad_hashes(hash_stream):
    queue = []

    for pair in hash_stream:
        queue.append(pair)

        while len(queue) > 1000:
            index, hash_value = queue.pop(0)

            if repeat := repeats_three(hash_value):
                if any(repeats_five(haystack, repeat) for (_, haystack) in queue):
                    yield index


def nth_item(iterable, n):
    """
    >>> nth_item(range(100), 17)
    17
    """

    return next(itertools.islice(iterable, n, n + 1))


def part1(data):
    """
    >>> part1('abc')
    22728
    >>> part1(SALT)
    16106
    """

    return nth_item(pad_hashes(hashes(data)), 63)


def part2(data):
    """
    >>> part2(SALT)
    22423
    """

    return nth_item(pad_hashes(stretched_hashes(data)), 63)


def main():
    print(part1(SALT))
    print(part2(SALT))


if __name__ == "__main__":
    main()
