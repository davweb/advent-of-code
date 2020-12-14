# -*- coding: utf-8 -*-

import re
from collections import defaultdict

PATTERN = re.compile(r"(\d+) <-> ((\d+, )*\d+)")

def read_input():
    file = open("input/2018/day20-input.txt", "r")
    return file.read().strip()


def doors(regex):
    """
    >>> doors("^WNE$")
    3
    >>> doors("^ENWWW(NEEE|SSE(EE|N))$")
    10
    >>> doors("^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$")
    18
    >>> doors("^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$")
    23
    >>> doors("^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$")
    31
    """

    groups = []
    group = [0]
    
    for i in regex:
        if i in ('N', 'S', 'E', 'W'):
            group[-1] += 1
        elif i == '(':
            groups.append(group)
            group = [0]
        elif i == '|':
            group.append(0)
        elif i == ')':
            length = 0 if min(group) == 0 else max(group)
            group = groups.pop()
            group[-1] += length

    return group[0]


def depth(limit, regex):
    """
    >>> depth(2, "^WNE$")
    2
    >>> depth(9, "^ENWWW(NEEE|SSE(EE|N))$")
    4
    
    # >>> doors("^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$")
    # 18
    # >>> doors("^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$")
    # 23
    # >>> doors("^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$")
    # 31
    """

    groups = []
    group = [0]
    depth = 0
    count = 0
    
    for i in regex:
        if i in ('N', 'S', 'E', 'W'):
            group[-1] += 1
            depth += 1

            print(i, depth)
            if depth >= limit:
                count += 1

        elif i == '(':
            groups.append(group)
            group = [0]
        elif i == '|':
            group.append(0)
        elif i == ')':
            length = 0 if min(group) == 0 else max(group)
            group = groups.pop()
            group[-1] += length

    return count



def part1(data):
    """
    >>> part1(read_input())
    3669
    """

    return doors(data)


def part2(data):
    """
    >>> part2(read_input())
    0
    """

    return 0


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
