import re
from enum import Enum

SPRING_LOCATION = (500, 0)

class Block(Enum):
    CLAY  = '#'
    WATER = '|'
    STILL_WATER = '~'
    SPRING = '+'


class Action(Enum):
    POUR  = 1
    SPREAD = 2


class Direction(Enum):
    LEFT  = -1
    RIGHT = 1


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
        >>> slice.count_blocks(Block.CLAY)
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
                self.grid[(x, y)] = Block.CLAY

        for groups in VERTICAL_PATTERN.findall(text):
            x = int(groups[0])
            y_from = int(groups[1])
            y_to = int(groups[2])

            for y in range(y_from, y_to + 1):
                self.grid[(x, y)] = Block.CLAY

        # pad X to show water flow to the side of the clay
        self.min_x = min(x for (x,y) in self.grid.keys()) - 3
        self.max_x = max(x for (x,y) in self.grid.keys()) + 3
        self.min_y = min(y for (x,y) in self.grid.keys())
        self.max_y = max(y for (x,y) in self.grid.keys())


    def count_blocks(self, block_type):
        return sum(1 for ((x, y), block) in self.grid.items() if block == block_type and y >= self.min_y)


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
        >>> slice.count_blocks(Block.WATER) + slice.count_blocks(Block.STILL_WATER)
        57
        >>> slice = Slice(
        ...     r"x=520, y=1..4\\n"
        ...     r"x=499, y=2..7\\n"
        ...     r"x=501, y=2..7\\n"
        ...     r"y=7, x=499..501\\n" 
        ...     r"x=496, y=8..10\\n"
        ...     r"x=504, y=5..10\\n"
        ...     r"y=10, x=497..503\\n" 
        ... )
        >>> slice.start_water()
        >>> slice.count_blocks(Block.WATER) + slice.count_blocks(Block.STILL_WATER)
        54
        >>> slice = Slice(
        ...     r"x=520, y=1..4\\n"
        ...     r"x=499, y=2..7\\n"
        ...     r"x=501, y=2..7\\n"
        ...     r"y=7, x=499..501\\n" 
        ...     r"x=496, y=8..10\\n"
        ...     r"x=504, y=5..10\\n"
        ...     r"y=10, x=497..503\\n" 
        ...     r"x=480, y=12..20\\n"
        ...     r"x=510, y=15..20\\n"
        ...     r"y=20, x=481..509\\n" 
        ... )
        >>> slice.start_water()
        >>> slice.count_blocks(Block.WATER) + slice.count_blocks(Block.STILL_WATER)
        242
        >>> slice = Slice(
        ...     r"x=520, y=1..4\\n"
        ...     r"x=499, y=6..8\\n"
        ...     r"x=501, y=6..8\\n"
        ...     r"y=8, x=499..501\\n" 
        ...     r"x=496, y=4..11\\n"
        ...     r"x=504, y=4..11\\n"
        ...     r"y=11, x=497..503\\n" 
        ... )
        >>> slice.start_water()
        >>> slice.count_blocks(Block.WATER) + slice.count_blocks(Block.STILL_WATER)
        71
        >>> slice = Slice(
        ...     r"x=520, y=1..4\\n"    
        ...     r"x=489, y=6..8\\n"
        ...     r"x=491, y=6..8\\n"
        ...     r"y=8, x=489..491\\n" 
        ...     r"x=486, y=4..11\\n"
        ...     r"x=514, y=4..11\\n"
        ...     r"y=11, x=487..513\\n" 
        ... )
        >>> slice.start_water()
        >>> slice.count_blocks(Block.WATER) + slice.count_blocks(Block.STILL_WATER)
        231
        >>> slice = Slice(
        ...     r"x=520, y=1..4\\n"
        ...     r"x=498, y=2..4\\n"
        ...     r"x=502, y=2..4\\n"
        ...     r"y=4, x=498..502\\n" 
        ...     r"x=486, y=6..11\\n"
        ...     r"x=502, y=6..11\\n"
        ...     r"y=11, x=487..502\\n" 
        ... )
        >>> slice.start_water()
        >>> slice.count_blocks(Block.WATER) + slice.count_blocks(Block.STILL_WATER)
        125
        """

        self.grid[SPRING_LOCATION] = Block.SPRING
        spring_x, spring_y = SPRING_LOCATION

        action_queue = []
        action_queue.append((Action.POUR, (spring_x, spring_y + 1)))

        while action_queue:
            action, location = action_queue.pop(0)
            x, y = location
            
            # Pour water downwards until we hit something
            if action == Action.POUR:
                while y <= self.max_y and self.grid.get((x, y)) is None:
                    self.grid[(x,y)] = Block.WATER
                    y += 1

                # If we hit sand or still water spread horizontally
                if y - 1 < self.max_y and self.grid.get((x, y)) != Block.WATER:
                    action_queue.append((Action.SPREAD, (x, y - 1)))

            # Spread horizontally until we hit something or can pour downwards
            elif action == Action.SPREAD:
                poured = False
                limit = {}

                # spread in both directions
                for direction in Direction:
                    i = x + direction.value

                    # spread until we hit clay
                    while self.grid.get((i, y)) != Block.CLAY:
                        self.grid[(i, y)] = Block.WATER

                        # if we can pour down then stop spreading and go down
                        if self.grid.get((i, y + 1)) is None:
                            action_queue.append((Action.POUR, (i, y + 1)))
                            poured = True
                            break

                        # if we hit water just stop
                        if self.grid.get((i, y + 1)) == Block.WATER:
                            poured = True
                            break

                        i += direction.value

                    limit[direction] = i

                # We've hit clay both sides
                if not poured:
                    # Mark still water
                    for still in range(limit[Direction.LEFT] + 1, limit[Direction.RIGHT]):
                        self.grid[(still, y)] = Block.STILL_WATER

                    # Spread one level up
                    self.grid[(x, y - 1)] = Block.WATER
                    action_queue.append((Action.SPREAD, (x, y - 1)))


    def __str__(self):
        output = ['     {}'.format(self.min_x)]

        for y in range(self.min_y, self.max_y + 1):
            row = []

            for x in range(self.min_x, self.max_x + 1):
                block = self.grid.get((x ,y))

                if block is None:
                    row.append('.')
                else:
                    row.append(block.value)

            output.append("{:4d} {}".format(y, "".join(row)))

        return "\n".join(output)


def part1(data):
    """
    >>> part1(read_input())
    31861
    """

    slice = Slice(data)
    slice.start_water()
    return slice.count_blocks(Block.WATER) + slice.count_blocks(Block.STILL_WATER)


def part2(data):
    """
    >>> part2(read_input())
    26030
    """

    slice = Slice(data)
    slice.start_water()
    return slice.count_blocks(Block.STILL_WATER)


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
