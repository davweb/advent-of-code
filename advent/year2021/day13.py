# -*- coding: utf-8 -*-

import re

DOT_PATTERN = re.compile(r'(\d+),(\d+)')
FOLD_PATTERN = re.compile(r'fold along (x|y)=(\d+)')


def read_input():

    with open('input/2021/day13-input.txt', encoding='utf8') as file:
        dots = []
        folds = []

        for line in file.readlines():
            if line.strip() == "":
                continue

            match = DOT_PATTERN.match(line)

            if match:
                dots.append((int(match.group(1)), int(match.group(2))))
                continue

            match = FOLD_PATTERN.match(line)

            if match:
                folds.append((match.group(1), int(match.group(2))))
                continue

            raise ValueError(line)

    return (dots, folds)


def fold_paper(paper, axis, fold):
    index = 0 if axis == 'x' else 1
    to_fold = [dot for dot in paper if dot[index] > fold]

    for dot in to_fold:
        paper.remove(dot)
        value = dot[index]
        value = fold - (value - fold)

        if index == 0:
            dot = (value, dot[1])
        else:
            dot = (dot[0], value)

        paper.add(dot)


def part1(data):
    """
    >>> part1(read_input())
    671
    """

    dots, folds = data
    paper = set(dots)
    axis, fold = folds[0]
    fold_paper(paper, axis, fold)
    return len(paper)


def part2(data):
    """
    >>> expected_result = '\\n'.join([
    ...    '███   ██  ███  █  █  ██  ███  █  █ █   ',
    ...    '█  █ █  █ █  █ █  █ █  █ █  █ █ █  █   ',
    ...    '█  █ █    █  █ ████ █  █ █  █ ██   █   ',
    ...    '███  █    ███  █  █ ████ ███  █ █  █   ',
    ...    '█    █  █ █    █  █ █  █ █ █  █ █  █   ',
    ...    '█     ██  █    █  █ █  █ █  █ █  █ ████'
    ... ])
    >>> part2(read_input()) == expected_result
    True
    """

    dots, folds = data
    paper = set(dots)

    for axis, fold in folds:
        fold_paper(paper, axis, fold)

    left = min(x for x, _ in paper)
    right = max(x for x, _ in paper)
    top = min(y for _, y in paper)
    bottom = max(y for _, y in paper)

    output = []

    for y in range(top, bottom + 1):
        row = ''

        for x in range(left, right + 1):
            dot = (x, y)
            row += '█' if dot in paper else ' '

        output.append(row)

    return "\n".join(output)


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
