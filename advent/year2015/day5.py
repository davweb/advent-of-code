from collections import Counter


def read_input():
    with open('input/2015/day5-input.txt', encoding='utf8') as file:
        return list(file)


def has_repeated_character(string):
    previous = string[0]

    for char in string[1:]:
        if previous == char:
            return True
        previous = char

    return False


def nice(string):
    """
    >>> nice("ugknbfddgicrmopn")
    True
    >>> nice("aaa")
    True
    >>> nice("abc")
    False
    >>> nice("jchzalrnumimnmhp")
    False
    >>> nice("haegwjzuvuyypxyu")
    False
    >>> nice("dvszwmarrgswjxmb")
    False
    """

    counter = Counter(string)
    vowels = sum(counter[vowel] for vowel in "aeiou")
    contains_forbidden = any(
        forbidden in string for forbidden in [
            'ab', 'cd', 'pq', 'xy'])
    return vowels >= 3 and has_repeated_character(
        string) and not contains_forbidden


def nicer(string):
    """
    >>> nicer("qjhvhtzxzqqjkmpb")
    True
    >>> nicer("xxyxx")
    True
    >>> nicer("uurcxstgmygtbstg")
    False
    >>> nicer("ieodomkazucvgmuy")
    False
    """

    pair = False

    for i in range(0, len(string) - 3):
        for j in range(i + 2, len(string) - 1):
            if string[i:i + 2] == string[j:j + 2]:
                pair = True
                break

    if not pair:
        return False

    for i in range(0, len(string) - 2):
        if string[i] == string[i + 2]:
            return True

    return False


def part1(data):
    """
    >>> part1(read_input())
    255
    """

    return sum(nice(string) for string in data)


def part2(data):
    """
    >>> part2(read_input())
    55
    """

    return sum(nicer(string) for string in data)


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
