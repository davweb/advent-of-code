#!/usr/local/bin/python3

import sys
from collections import defaultdict

def play(players, last_marble):
    """
    >>> play(9, 25)
    32
    >>> play(10, 1618)
    8317
    >>> play(13, 7999)
    146373
    >>> play(17, 1104)
    2764
    >>> play(21, 6111)
    54718
    >>> play(30, 5807)
    37305
    """

    ring = [0, 1]
    index = 1
    scores = defaultdict(int)
    player = 1

    for marble in range(2, last_marble + 1):
        player = (player + 1) % players

        if marble % 23 == 0:
            index = (index - 7) % len(ring)
            scores[player] += marble + ring[index]
            del ring[index]
        else:
            index = (index + 2) % len(ring)
            ring.insert(index, marble)  
    
    return max(score for score in scores.values())

class Marble:
    def __init__(self, value):
        self.value = value
        self.next = self
        self.previous = self

    def forward(self, count = 1):
        """
        >>> a = Marble(1)
        >>> b = Marble(2)
        >>> c = Marble(3)
        >>> c.insert(b)
        Marble(2)
        >>> b.insert(a)
        Marble(1)
        >>> a.forward(0)
        Marble(1)
        >>> a.forward(1)
        Marble(2)
        >>> a.forward(2)
        Marble(3)
        """
        
        return self if count == 0 else self.next.forward(count - 1)
    
    def back(self, count = 1):
        """
        >>> a = Marble(1)
        >>> b = Marble(2)
        >>> c = Marble(3)
        >>> c.insert(b)
        Marble(2)
        >>> b.insert(a)
        Marble(1)
        >>> c.back(0)
        Marble(3)
        >>> c.back(1)
        Marble(2)
        >>> c.back(2)
        Marble(1)
        """

        return self if count == 0 else self.previous.back(count - 1)

    def insert(self, other):
        """
        >>> a = Marble(1)
        >>> b = Marble(2)
        >>> b.insert(a)
        Marble(1)
        >>> c = Marble(3)
        >>> b.insert(c)
        Marble(3)
        >>> c.forward()
        Marble(2)
        >>> c.back()
        Marble(1)
        """
        previous = self.previous
        previous.next = other
        other.previous = previous
        other.next = self
        self.previous = other
        return other

    def remove(self):
        """
        >>> a = Marble(1)
        >>> b = Marble(2)
        >>> c = Marble(3)
        >>> c.insert(b)
        Marble(2)
        >>> b.insert(a)
        Marble(1)
        >>> b.remove()
        Marble(3)
        >>> c.back()
        Marble(1)
        >>> a.forward()
        Marble(3)
        """

        self.previous.next = self.next
        self.next.previous = self.previous
        return self.next

    def __repr__(self):
        return 'Marble({})'.format(self.value)

def play_new(players, last_marble, progress=False):
    """
    >>> play_new(9, 25)
    32
    >>> play_new(10, 1618)
    8317
    >>> play_new(13, 7999)
    146373
    >>> play_new(17, 1104)
    2764
    >>> play_new(21, 6111)
    54718
    >>> play_new(30, 5807)
    37305
    """

    zero = Marble(0)
    one = Marble(1)
    current = zero.insert(one)
    scores = defaultdict(int)
    player = 1
    inc = 2 if last_marble < 200 else (last_marble // 200)

    for marble in range(2, last_marble + 1):
        if progress and (marble % inc == 0):
            print("{:3.0f}%".format(marble / last_marble * 100), end = "\r", file=sys.stderr)

        player = (player + 1) % players

        if marble % 23 == 0:
            current = current.back(7)
            scores[player] += marble + current.value
            current = current.remove()
        else:
            current = current.forward(2)
            current = current.insert(Marble(marble))
    
    if progress:
        print("Done!", file=sys.stderr)
    return max(score for score in scores.values())


def part1(players, last_marble):
    """
    >>> part1(468, 71010)
    374287
    """

    return play(players, last_marble)

def part2(players, last_marble, progress=False):
    """
    >>> part2(468, 71010)
    3083412635
    """
    return play_new(players, last_marble * 100, progress=progress)

def main():
    # 468 players; last marble is worth 71010 points
    print(part1(468, 71010))
    print(part2(468, 71010, progress=True))

if __name__ == "__main__":
    main()
    