# -*- coding: utf-8 -*-


def read_input(filename='input/2023/day9-input.txt'):
    with open(filename, encoding='utf8') as file:
        for line in file:
            yield [int(i) for i in line.split()]


def predict(values, add):
    """
    >>> predict([[0, 3, 6, 9, 12, 15]], True)
    18
    >>> predict([[0, 3, 6, 9, 12, 15]], False)
    -3
    """

    differences = [n - values[0][i] for i, n in enumerate(values[0][1:])]

    if not any(differences):
        last_value = 0

        for previous_list in values:
            last_value = previous_list[-1] + last_value if add else previous_list[0] - last_value

        return last_value

    values.insert(0, differences)
    return predict(values, add)


def part1(data):
    """
    >>> part1(read_input())
    1884768153
    """

    return sum(predict([values], True) for values in data)


def part2(data):
    """
    >>> part2(read_input())
    1031
    """

    return sum(predict([values], False) for values in data)


def main():
    print(part1(read_input()))
    print(part2(read_input()))


if __name__ == "__main__":
    main()
