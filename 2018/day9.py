#!/usr/local/bin/python3

from collections import defaultdict

def play(players, last_marble):
    """
    >>> play(1, 100)
    32
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

def part1(players, last_marble):
    print(play(players, last_marble))

def part2(players, last_marble):
    print(play(players, last_marble * 100))

def main():
    # 468 players; last marble is worth 71010 points
    part1(468, 71010)
    part2(468, 71010)

if __name__ == "__main__":
    main()
    