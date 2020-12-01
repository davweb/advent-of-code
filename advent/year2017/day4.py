#!/usr/local/bin/python3

def read_input():
    file = open('input/2017/day4-input.txt', 'r')
    return [line.split() for line in file]


def part1(data):
    """
    >>> part1([['aa','bb','cc','dd','ee']])
    1
    >>> part1([['aa','bb','cc','dd','aa']])
    0
    >>> part1([['aa','bb','cc','dd','aaa']])
    1
    >>> part1(read_input())
    451
    """
   
    valid = 0

    for words in data:
        unique = set(words)
        if len(words) == len(unique):
            valid += 1

    return valid


def part2(data):
    """
    >>> part2([['abcde','fghij']])
    1
    >>> part2([['abcde','xyz','ecdab']])
    0
    >>> part2(read_input())
    223
    """

    valid = 0

    for words in data:
        words = [''.join(sorted(word)) for word in words]
        unique = set(words)
        if len(words) == len(unique):
            valid += 1

    return valid


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
