import sys
import re
from enum import Enum

sys.setrecursionlimit(5000)

class Block(Enum):
    ROCK  = '#'
    WATER = 'W'
    SPRING = '+'

HORIZONTAL_PATTERN = re.compile(r"y=(\d+), x=(\d+)..(\d+)")
VERTICAL_PATTERN = re.compile(r"x=(\d+), y=(\d+)..(\d+)")

def read_input():
    file = open('input/2018/day17-input.txt', 'r')
    return file.read()


class Slice:

    def __init__(self, text):
        """
        >>> slice = Slice(
        ...     r"x=495, y=2..7\\n"
        ...     r"y=7, x=495..501\\n"
        ...     r"x=501, y=3..7\\n"
        ...     r"x=498, y=2..4\\n"
        ...     r"x=506, y=1..2\\n"
        ...     r"x=498, y=10..13\\n"
        ...     r"x=504, y=10..13\\n"
        ...     r"y=13, x=498..504\\n"
        ... )
        >>> slice.count_blocks(Block.SPRING)
        1
        >>> slice.count_blocks(Block.ROCK)
        34
        >>> slice.count_blocks(Block.WATER)
        0
        """

        self.grid = {}

        for groups in HORIZONTAL_PATTERN.findall(text):
            y = int(groups[0])
            x_from = int(groups[1])
            x_to = int(groups[2])

            for x in range(x_from, x_to + 1):
                self.grid[(x, y)] = Block.ROCK

        for groups in VERTICAL_PATTERN.findall(text):
            x = int(groups[0])
            y_from = int(groups[1])
            y_to = int(groups[2])

            for y in range(y_from, y_to + 1):
                self.grid[(x, y)] = Block.ROCK

        self.grid[(500, 0)] = Block.SPRING

        # pad X to allow water flow to the side of rocks
        self.min_x = min(x for (x,y) in self.grid.keys()) - 1
        self.max_x = max(x for (x,y) in self.grid.keys()) + 1
        self.min_y = min(y for (x,y) in self.grid.keys())
        self.max_y = max(y for (x,y) in self.grid.keys())


    def count_blocks(self, block_type):
        return sum(1 for block in self.grid.values() if block == block_type)


    def start_water(self):
        """
        >>> slice = Slice(
        ...     r"x=495, y=2..7\\n"
        ...     r"y=7, x=495..501\\n"
        ...     r"x=501, y=3..7\\n"
        ...     r"x=498, y=2..4\\n"
        ...     r"x=506, y=1..2\\n"
        ...     r"x=498, y=10..13\\n"
        ...     r"x=504, y=10..13\\n"
        ...     r"y=13, x=498..504\\n"
        ... )
        >>> slice.start_water()
        >>> slice.count_blocks(Block.WATER)
        57
        >>> print(slice)
        """

        spring_x, spring_y = next(location for (location, block) in self.grid.items() if block == Block.SPRING)
        self.pour((spring_x, spring_y + 1))

    
    def pour(self, location):
        x, y = location

        # We've finished when we hit the bottom
        if y > self.max_y:
            return True

        block = self.grid.get(location)

        # Can't pour into filled squares
        if block is not None or block == Block.WATER:
            return False

        self.grid[location] = Block.WATER

        if self.pour((x, y + 1)):
            return True

        left = self.pour((x - 1, y))
        right = self.pour((x + 1, y))

        return left or right
    

    def __str__(self):
        output = ['    {}'.format(self.min_x)]

        for y in range(self.min_y, self.max_y + 1):
            row = []

            for x in range(self.min_x, self.max_x + 1):
                block = self.grid.get((x ,y))

                if block is None:
                    row.append('.')
                else:
                    row.append(block.value)

            output.append("{:3d} {}".format(y, "".join(row)))

        return "\n".join(output)


def part1(data):
    """
    >>> part1(read_input())
    0

    < 72646
    """
    
    # slice = Slice(data)
    # slice.start_water()
    # print(slice)
    # return slice.count_blocks(Block.WATER)
    return 0


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
