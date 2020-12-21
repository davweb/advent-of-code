import re
import math
from enum import Enum


TILE_PATTERN = re.compile(r'Tile (\d+):\n(([.#]{10}\n){10})', re.MULTILINE)
SEA_MONSTER = (
    '                  # ',
    '#    ##    ##    ###',
    ' #  #  #  #  #  #   '
)

def rotations(rows):
    """
    >>> rotations(('...', '###', '#.#'))
    [('...', '###', '#.#'), ('##.', '.#.', '##.'), ('#.#', '###', '...'), ('.##', '.#.', '.##')]
    """

    rotations = []

    for _ in range(4):
        rotations.append(rows)
        rows = tuple("".join(row) for row in zip(*rows[::-1]))

    return rotations


def flips(rows):
    """
    >>> flips(('...', '###', '#..'))
    [('...', '###', '#..'), ('#..', '###', '...'), ('...', '###', '..#')]
    """

    flips = []
    flips.append(rows)
    flips.append(reversed(rows))
    flips.append(reversed(row) for row in rows)

    return [tuple("".join(row) for row in flip) for flip in flips]


def permutations(rows):
    """
    >>> permutations(['...', '###', '#..'])
    [('##.', '.#.', '.#.'), ('#..', '###', '...'), ('.##', '.#.', '.#.'), ('.#.', '.#.', '##.'), ('.#.', '.#.', '.##'), ('..#', '###', '...'), ('...', '###', '#..'), ('...', '###', '..#')]
    """

    result = set()

    for rotation in rotations(rows):
        for flip in flips(rotation):
            result.add(flip)

    return sorted(result)


class Side(Enum):
    TOP = 1
    BOTTOM = 2
    LEFT = 3
    RIGHT = 4


class Tile:
    """
    >>> tile = Tile(17, ('...', '###', '#..'))
    >>> tile.tile_id
    17
    >>> tile.next()
    ('##.', '.#.', '.#.')
    >>> tile.next()
    ('#..', '###', '...')
    >>> [tile.next() for _ in range(7)]
    Traceback (most recent call last):
    ...
    ValueError: Tile does not have another permutation
    """

    def __init__(self, tile_id, rows):
        self.tile_id = tile_id
        self.permutations = permutations(rows)
        self.reset()


    def rows(self):
        if self.state == -1:
            raise ValueError("Tile is not aligned")
        return self.permutations[self.state]


    def reset(self):
        self.state = -1


    def has_next(self):
        return self.state < len(self.permutations) - 1


    def next(self):
        if not self.has_next():
            raise ValueError("Tile does not have another permutation")

        self.state += 1
        return self.rows()


    def side(self, side):
        """
        >>> tile = Tile(17, ('##.', '.#.', '.#.'))
        >>> tile.next()
        ('##.', '.#.', '.#.')
        >>> tile.side(Side.TOP)
        '##.'
        >>> tile.side(Side.BOTTOM)
        '.#.'
        >>> tile.side(Side.LEFT)
        '#..'
        >>> tile.side(Side.RIGHT)
        '...'
        """

        if side == Side.TOP:
            return self.rows()[0]
        elif side == Side.BOTTOM:
            return self.rows()[-1]
        elif side == Side.LEFT:
            return "".join(row[0] for row in self.rows())
        elif side == Side.RIGHT:
            return "".join(row[-1] for row in self.rows())
        else:
            raise ValueError("Unknown side '{}'".format(side))


    def matches(self, side, other):
        """
        >>> tile = Tile(17, ('##.', '.#.', '.#.'))
        >>> tile.next()
        ('##.', '.#.', '.#.')
        >>> other = Tile(22, ('.#.', '.#.', '.#.'))
        >>> other.next()
        ('.#.', '.#.', '.#.')
        >>> tile.matches(Side.TOP, other)
        False
        >>> tile.matches(Side.BOTTOM, other)
        True
        >>> tile.matches(Side.LEFT, other)
        False
        >>> tile.matches(Side.RIGHT, other)
        True
        """
        this_row = self.side(side)

        if side == Side.TOP:
            other_row = other.side(Side.BOTTOM)
        elif side == Side.BOTTOM:
            other_row = other.side(Side.TOP)
        elif side == Side.LEFT:
            other_row = other.side(Side.RIGHT)
        elif side == Side.RIGHT:
            other_row = other.side(Side.LEFT)
        else:
            raise ValueError("Unknown side '{}'".format(side))

        return this_row == other_row


def read_input():
    file = open('input/2020/day20-input.txt', 'r')
    text = file.read()

    tiles = set()

    for groups in TILE_PATTERN.findall(text):
        tile_id = int(groups[0])
        rows = groups[1].strip().split("\n")
        tiles.add(Tile(tile_id, rows))

    return tiles


def fit(size, tiles, grid, x, y):
    next_x = x + 1

    if next_x == size:
        next_x = 0
        next_y = y + 1
    else:
        next_y = y

    for tile in list(tiles):
        tile.reset()

        while tile.has_next():
            tile.next()

            if x > 0 and not tile.matches(Side.LEFT, grid[(x - 1, y)]):
                continue
            if y > 0 and not tile.matches(Side.TOP, grid[(x, y - 1)]):
                continue

            grid[(x, y)] = tile
            tiles.remove(tile)

            if next_y == size:
                return True

            if fit(size, tiles, grid, next_x, next_y):
                return True

            tiles.add(tile)
            del grid[(x, y)]

    return False


def sea_monsters(pattern):
    """
    >>> sea_monsters([
    ...     '....................O...',
    ...     '#.O.##.OO#.#.OO.##.OOO##',
    ...     '..#O.#O#.O##O..O.#O##.##',
    ...     '...#.#..##.##...#..#..##'
    ... ])
    (1, 29)
    >>> sea_monsters([
    ...     '.###.#..####...##..#....',
    ...     '#.###...#.##...#.##O###.',
    ...     '.O##.#OO.###OO##..OOO##.',
    ...     '..O#.O..O..O.#O##O##.###',
    ...     '#.#..##.########..#..##.'
    ... ])
    (1, 58)
    >>> sea_monsters([
    ...     '.###.#..####...##..#....',
    ...     '#.###...#.##...#.######.',
    ...     '.###.###.#######..#####.',
    ...     '..##.#..#..#.#######.###',
    ...     '#.#..##.########..#..##.'
    ... ])
    (1, 58)
    >>> sea_monsters([
    ...     '.###.#..####...##..#....',
    ...     '.###.###.#######..#####.',
    ...     '#.###...#.##...#.######.',
    ...     '..##.#..#..#.#######.###',
    ...     '#.#..##.########..#..##.'
    ... ])
    (0, 73)
    """

    height = len(SEA_MONSTER)
    width = len(SEA_MONSTER[0])
    count = 0

    pattern = [list(row) for row in pattern]

    for y in range(0, len(pattern) - height + 1):
        for x in range(0, len(pattern[y]) - width + 1):
            match = True

            for row in range(0, height):
                for column in range(0, width):
                    if SEA_MONSTER[row][column] == '#' and not pattern[y + row][x + column] in ('O', '#'):
                        match = False
                        break

                if not match:
                    break

            if match:
                count += 1

                for row in range(0, height):
                    for column in range(0, width):
                        if SEA_MONSTER[row][column] == '#':
                            pattern[y + row][x + column] = 'O'

    hashes = 0

    for y in range(0, len(pattern)):
        for x in range(0, len(pattern[y])):
            if pattern[y][x] == '#':
                hashes += 1

    return (count, hashes)


def part1and2(tiles):
    """
    >>> part1and2(read_input())
    (79412832860579, 2155)
    """

    size = int(math.sqrt(len(tiles)))
    grid = {}
    fit(size, tiles, grid, 0, 0)

    edge = size - 1
    corners = math.prod(grid[location].tile_id for location in ((0, 0), (edge, 0), (0, edge), (edge, edge)))

    pattern = []

    for y in range(0, size):
        for row in range(1, 9):
            line = ""

            for x in range (0, size):
                tile = grid[(x,y)]
                line += tile.rows()[row][1:-1]

            pattern.append(line)

    roughness = None

    for permutation in permutations(pattern):
        (monsters, roughness) = sea_monsters(permutation)
        if monsters > 0:
            break

    return (corners, roughness)


def main():
    print(part1and2(read_input()))


if __name__ == "__main__":
    main()
