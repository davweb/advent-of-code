# -*- coding: utf-8 -*-

INPUT = "716892543"
from collections import deque


def play(cups, turns):
    """
    >>> cups = play("389125467", 10)
    >>> "".join(str(cup) for cup in cups)
    '192658374'
    >>> cups = play("389125467", 100)
    >>> "".join(str(cup) for cup in cups)
    '167384529'
    """

    cups = deque(int(cup) for cup in cups)
    min_cup = min(cups)
    max_cup = max(cups)

    current = cups[0]
    current_index = cups.index(current)
    turn = 0

    while turn < turns:
        turn += 1
        
        # pick up three cups
        cups.rotate(- current_index - 1)
        holding = []

        for _ in range(3):
            holding.append(cups.popleft())

        # pick the destination cup
        destination = current - 1
        if destination < min_cup:
            destination = max_cup

        while destination in holding:
            destination = destination - 1
            if destination < min_cup:
                destination = max_cup

        # put the cups back
        destination_index = cups.index(destination)
        cups.rotate(- destination_index - 1)
        cups.extendleft(reversed(holding))

        # pick the next cup
        current_index = cups.index(current)
        current_index += 1

        if current_index == len(cups):
            current_index = 0

        current = cups[current_index]

    cups.rotate(- cups.index(1))
    return cups


def part1(data):
    """
    >>> part1(INPUT)
    '49725386'
    """

    cups = play(data, 100)
    cups.popleft()
    return "".join(str(cup) for cup in cups)


def part2(cups):
    """
    # >>> part2(INPUT)
    # 538935646702
    #
    # (540847, 996466, 538935646702)
    """

    cups = [int(cup) for cup in cups]
    next_cup = max(cups) + 1
    cups += range(next_cup, 1000001)
    cups = play(cups, 10000000)

    cups.popleft()
    a = cups.popleft()
    b = cups.popleft()
    return a * b


def main():
    print(part1(INPUT))
    # print(part2(INPUT))


if __name__ == "__main__":
    main()
