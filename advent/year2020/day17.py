# -*- coding: utf-8 -

def read_input():
    file = open('input/2020/day17-input.txt', 'r')
    return file.read()


class Dimension:
    def __init__(self, text):
        self.cycle = 0
        self.map = set()

        for y, row in enumerate(text.strip().split("\n")):
            for x, cell in enumerate(row):
                if cell == '#':
                    self.map.add((x, y, 0))

    
    def coordinate_range(self, index):
        min_val = min(c[index] for c in self.map)
        max_val = max(c[index] for c in self.map)
        return range(min_val - 1, max_val + 2)


    def x_range(self):
        return self.coordinate_range(0)


    def y_range(self):
        return self.coordinate_range(1)


    def z_range(self):
        return self.coordinate_range(2)


    def get(self, *coordinate):
        return coordinate in self.map


    def adjacent_cells(self, x, y, z):
        for dx in (-1 , 0, 1):
            for dy in (-1 , 0, 1):
                for dz in (-1 , 0, 1):
                    if (dx == dy == dz == 0):
                        continue
                    
                    yield (x + dx, y + dy, z + dz)


    def count_adjacent_active(self, *coordinate):
        """
        >>> dimension = Dimension(".#.\\n##|\\n.##\\n")
        >>> dimension.count_adjacent_active(1, 1, 0)
        4
        """

        return sum(1 for c in self.adjacent_cells(*coordinate) if self.get(*c))


    def process(self):
        new_map = set()

        for z in self.z_range():

            for y in self.y_range():

                for x in self.x_range():
                    is_active = self.get(x, y, z)

                    if is_active:
                        if self.count_adjacent_active(x, y, z) not in (2, 3):
                            is_active = False
                    else:
                        if self.count_adjacent_active(x, y, z) == 3:
                            is_active = True

                    if is_active:
                        new_map.add((x, y, z))

        self.map = new_map
        self.cycle += 1


    def run(self, cycles):
        while self.cycle < cycles:
            self.process()


    def count_active(self):
        """
        >>> dimension = Dimension(".#.\\n##|\\n.##\\n")
        >>> dimension.count_active()
        5
        """

        return len(self.map)


class FourDimension(Dimension):
    def __init__(self, text):
        self.cycle = 0
        self.map = set()

        for y, row in enumerate(text.strip().split("\n")):
            for x, cell in enumerate(row):
                if cell == '#':
                    self.map.add((x, y, 0, 0))

    
    def w_range(self):
        return self.coordinate_range(3)


    def adjacent_cells(self, x, y, z, w):
        for dx in (-1 , 0, 1):
            for dy in (-1 , 0, 1):
                for dz in (-1 , 0, 1):
                    for dw in (-1 , 0, 1):
                        if (dx == dy == dz == dw == 0):
                            continue
                    
                        yield (x + dx, y + dy, z + dz, w + dw)


    def process(self):
        new_map = set()

        for z in self.z_range():

            for y in self.y_range():

                for x in self.x_range():

                    for w in self.w_range():
                        is_active = self.get(x, y, z, w)

                        if is_active:
                            if self.count_adjacent_active(x, y, z, w) not in (2, 3):
                                is_active = False
                        else:
                            if self.count_adjacent_active(x, y, z, w) == 3:
                                is_active = True

                        if is_active:
                            new_map.add((x, y, z, w))

        self.map = new_map
        self.cycle += 1


def part1(data):
    """
    >>> part1(read_input())
    386
    """

    dimension = Dimension(data)
    dimension.run(6)
    return dimension.count_active()


def part2(data):
    """
    >>> part2(read_input())
    2276
    """
    
    dimension = FourDimension(data)
    dimension.run(6)
    return dimension.count_active()


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
