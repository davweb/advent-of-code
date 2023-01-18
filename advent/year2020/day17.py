# -*- coding: utf-8 -

from itertools import product

OPTIONS = (-1, 0, 1)


def read_input():
    with open('input/2020/day17-input.txt', encoding='utf8') as file:
        return file.read()


class Dimension:
    def __init__(self, text):
        self.cycle = 0
        self.map = set()
        self.initialise(text)

    def initialise(self, text):
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

    def get(self, location):
        return location in self.map

    def adjacent_cells(self, location):
        x, y, z = location

        for dx, dy, dz in product(OPTIONS, OPTIONS, OPTIONS):
            if dx == dy == dz == 0:
                continue

            yield (x + dx, y + dy, z + dz)

    def count_adjacent_active(self, location):
        """
        >>> dimension = Dimension(".#.\\n##|\\n.##\\n")
        >>> dimension.count_adjacent_active((1, 1, 0))
        4
        """

        return sum(1 for c in self.adjacent_cells(location) if self.get(c))

    def all_locations(self):
        return product(self.x_range(), self.y_range(), self.z_range())

    def process(self):
        new_map = set()

        for location in self.all_locations():
            is_active = self.get(location)

            if is_active:
                if self.count_adjacent_active(location) not in (2, 3):
                    is_active = False
            else:
                if self.count_adjacent_active(location) == 3:
                    is_active = True

            if is_active:
                new_map.add(location)

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
    def initialise(self, text):
        for y, row in enumerate(text.strip().split("\n")):
            for x, cell in enumerate(row):
                if cell == '#':
                    self.map.add((x, y, 0, 0))

    def w_range(self):
        return self.coordinate_range(3)

    def adjacent_cells(self, location):
        x, y, z, w = location

        for dx, dy, dz, dw in product(OPTIONS, OPTIONS, OPTIONS, OPTIONS):
            if dx == dy == dz == dw == 0:
                continue

            yield (x + dx, y + dy, z + dz, w + dw)

    def all_locations(self):
        return product(self.x_range(), self.y_range(), self.z_range(), self.w_range())


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
