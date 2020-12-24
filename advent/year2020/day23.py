# -*- coding: utf-8 -*-

INPUT = "716892543"
from collections import deque

def slice(loop, index, length):
    """
    >>> a = [0, 1, 2, 3, 4, 5]
    >>> slice(a, 1, 2)
    [1, 2]
    >>> a
    [0, 3, 4, 5]
    >>> a = [0, 1, 2, 3, 4, 5]
    >>> slice(a, 4, 4)
    [4, 5, 0, 1]
    >>> a
    [2, 3]
    >>> a = [3, 4, 6, 7, 2, 5, 8, 9, 1]
    >>> slice(a, 7, 3)
    [9, 1, 3]
    >>> a
    [4, 6, 7, 2, 5, 8]
    """

    end = index + length
    repeat = end - len(loop)

    cut = loop[index:end]
    loop[index:end] = []
    
    if repeat >= 0:
        cut += loop[0:repeat]
        loop[0:repeat] = []

    return cut


def slice_deque(loop, index, length):
    """
    >>> a = deque([0, 1, 2, 3, 4, 5])
    >>> slice_deque(a, 1, 2)
    [1, 2]
    >>> list(a)
    [0, 3, 4, 5]
    >>> a = deque([0, 1, 2, 3, 4, 5])
    >>> slice_deque(a, 4, 4)
    [4, 5, 0, 1]
    >>> list(a)
    [2, 3]
    >>> a = deque([3, 4, 6, 7, 2, 5, 8, 9, 1])
    >>> slice_deque(a, 7, 3)
    [9, 1, 3]
    >>> list(a)
    [4, 6, 7, 2, 5, 8]
    >>> a = deque([3, 4, 6, 7, 2, 5, 8, 9, 1])
    >>> slice_deque(a, 7, 5)
    [9, 1, 3, 4, 6]
    >>> list(a)
    [7, 2, 5, 8]
    """

    delta = index + length - len(loop)
    if delta < 0:
        delta = 0

    loop.rotate(-index)
    cut = []

    for _ in range(length):
        cut.append(loop.popleft())

    loop.rotate(index - delta)


    return cut

def play(cups, turns):
    """
    >>> play("389125467", 10)
    '92658374'
    >>> play("389125467", 100)
    '67384529'
    """

    cups = [int(cup) for cup in cups]
    min_cup = min(cups)
    max_cup = max(cups)

    current = cups[0]
    current_index = cups.index(current)
    turn = 0

    while turn < turns:
        turn +=1
        
        # pick up three cups
        holding = slice(cups, current_index + 1, 3)

        # pick the destination cup
        destination = current - 1
        if destination < min_cup:
            destination = max_cup

        while destination not in cups:
            destination = destination - 1
            if destination < min_cup:
                destination = max_cup

        # put the cups back
        destination_index = cups.index(destination) + 1
        cups[destination_index:destination_index] = holding
        
        # pick the next cup
        current_index = cups.index(current)
        current_index += 1

        if current_index == len(cups):
            current_index = 0

        current = cups[current_index]

    start = cups.index(1)
    result = cups[start + 1:] + cups[:start]
    return "".join(str(cup) for cup in result)


def play_deque(cups, turns):
    """
    >>> play_deque("389125467", 10)
    (9, 2, 18)
    >>> play_deque("389125467", 100)
    (6, 7, 42)
    """

    cups = deque(int(cup) for cup in cups)
    min_cup = min(cups)
    max_cup = max(cups)

    current = cups[0]
    current_index = cups.index(current)
    turn = 0

    while turn < turns:
        turn +=1

        if turn % 1000 == 0:
            print(turn)
        
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

    start = cups.index(1)
    cups.rotate(-start - 1)

    a = cups.popleft()
    b = cups.popleft()

    return (a, b, a * b)


def part1(data):
    """
    >>> part1(INPUT)
    '49725386'
    """

    return play(data, 100)


def part2(cups):
    """
    # >>> part2(INPUT)
    # 0
    """

    cups = [int(cup) for cup in cups]
    next_cup = max(cups) + 1
    cups += range(next_cup, 1000001)
    return play_deque(cups, 10000000)


def main():
    # print(part1(INPUT))
    print(part2(INPUT))


if __name__ == "__main__":
    main()
