#!/usr/local/bin/python3

from collections import defaultdict
import re

PATTERN = re.compile(r"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)")

class Claim:

    def __init__(self, definition):
        """
        >>> Claim("#1355 @ 102,538: 21x28")
        Claim(id=1355, x=102, y=538, width=21, height=28)
        >>> Claim("a")
        Traceback (most recent call last):
        ...
        ValueError: Invalid defintion 'a'
        """

        match = PATTERN.match(definition)
        if not match:
            raise ValueError("Invalid defintion '{}'".format(definition))
        self.id = int(match.group(1))
        self.x = int(match.group(2))
        self.y = int(match.group(3))
        self.width = int(match.group(4))
        self.height = int(match.group(5))
    
    def squares(self):
        """
        >>> list(Claim("#1 @ 0,0: 2x2").squares())
        [(0, 0), (0, 1), (1, 0), (1, 1)]
        >>> list(Claim("#2 @ 3,2: 1x1").squares())
        [(3, 2)]
        >>> list(Claim("#3 @ 4,4: 1x3").squares())
        [(4, 4), (4, 5), (4, 6)]
        >>> list(Claim("#4 @ 4,4: 3x1").squares())
        [(4, 4), (5, 4), (6, 4)]
        """

        for x in range(self.x, self.x + self.width):
            for y in range(self.y, self.y + self.height):
                yield (x, y)

    def __repr__(self):
        return "Claim(id={id}, x={x}, y={y}, width={width}, height={height})".format(**self.__dict__)

def read_input():
    file = open('input/2018/day3-input.txt', 'r')
    return [Claim(line) for line in file.readlines()]

def part1(claims):
    """
    >>> part1(read_input())
    116491
    """
    grid = defaultdict(int)

    for claim in claims:
        for square in claim.squares():
            grid[square] += 1 

    return sum(1 for value in grid.values() if value >= 2)

def part2(claims):
    """
    >>> part2(read_input())
    707
    """
    

    grid = defaultdict(int)

    for claim in claims:
        for square in claim.squares():
            grid[square] += 1 

    for claim in claims:
        winner = True

        for square in claim.squares():
            if grid[square] > 1:
                winner = False
                break

        if winner:
            return claim.id

def main():
    claims = read_input()
    print(part1(claims))
    print(part2(claims))

if __name__ == "__main__":
    main()
