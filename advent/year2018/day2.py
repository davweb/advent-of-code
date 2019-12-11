#!/usr/local/bin/python3

import collections
import itertools

def read_input():
    file = open('input/2018/day2-input.txt', 'r')
    return list(line.strip() for line in file.readlines())

def count_letters(label):
    """
    >>> count_letters('aaa')
    {'a': 3}
    >>> count_letters('abaa')
    {'a': 3, 'b': 1}
    """
    count = collections.defaultdict(int)

    for letter in label:
        count[letter] += 1

    return dict(count)

def has_count(label, count):
    """
    >>> has_count('abcdef', 2)
    False
    >>> has_count('', 2)
    False
    >>> has_count('bababc', 2)
    True
    >>> has_count('bababc', 3)
    True
    >>> has_count('abbcde', 2)
    True
    >>> has_count('abcccd', 2)
    False
    >>> has_count('aabcdd', 2)
    True
    >>> has_count('aabcdd', 3)
    False
    >>> has_count('abcdee', 2)
    True
    >>> has_count('ababab', 2)
    False
    >>> has_count('ababab', 3)
    True
    """

    return count in count_letters(label).values()

def different_letter_count(first, second):
    """
    >>> different_letter_count('aaaa', 'aaa')
    Traceback (most recent call last):
        ...
    ValueError: labels are not the same length "aaaa", "aaa"
    >>> different_letter_count('aab', 'aaa')
    1
    >>> different_letter_count('abc', 'def')
    3
    """

    if len(first) != len(second):
        raise ValueError('labels are not the same length "{}", "{}"'.format(first, second))

    return sum(a != b for (a,b) in zip(first, second))

def part1(data):
    """
    >>> part1(read_input())
    6916
    """
    
    twos = 0
    threes = 0
    
    for label in data:
        if has_count(label, 2):
            twos += 1
        if has_count(label, 3):
            threes += 1

    return twos * threes

def part2(data):
    """
    >>> part2(read_input())
    'oeylbtcxjqnzhgyylfapviusr'
    """

    for (first, second) in itertools.product(data, data):
        if different_letter_count(first, second) == 1:
            return "".join(a for (a, b) in zip(first,second) if a == b)


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))

if __name__ == "__main__":
    main()
