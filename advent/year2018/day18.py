from enum import Enum

class Acre(Enum):
    TREE = '|'
    LUMBERYARD = '#'


def read_input():
    file = open('input/2018/day18-input.txt', 'r')
    return file.read()


class Forest:
    def __init__(self, text):
        self.minute = 0
        self.map = {}

        x = 0
        y = 0

        for y, row in enumerate(text.strip().split("\n")):
            for x, cell in enumerate(row):
                if cell == Acre.TREE.value:
                    acre = Acre.TREE
                elif cell == Acre.LUMBERYARD.value:
                    acre = Acre.LUMBERYARD
                elif cell == '.':
                    acre = None
                else:
                    raise ValueError("Invalid Forest acre '{}'".format(cell))

                self.set(x,y, acre)
        
        self.width = x + 1
        self.height = y + 1


    def get(self, x, y):
        return self.map.get((x, y))


    def set(self, x, y, acre):
        self.map[(x, y)] = acre


    def adjacent_cells(self, x, y):
        return ((x - 1, y - 1), (x, y - 1), (x + 1, y - 1), (x - 1, y), (x + 1, y), (x - 1, y + 1), (x, y + 1), (x + 1, y + 1))


    def count_adjacent(self, acre_x, acre_y, acre):
        """
        >>> forest = Forest("|#.\\n##|\\n.##\\n")
        >>> forest.count_adjacent(1, 1, Acre.TREE)
        2
        >>> forest.count_adjacent(1, 1, Acre.LUMBERYARD)
        4
        """

        return sum(1 for (x, y) in self.adjacent_cells(acre_x, acre_y) if self.get(x, y) == acre)

    
    def process(self):
        new_map = {}

        for y in range(0, self.height):

            for x in range(0, self.width):
                acre = self.get(x, y)

                if acre is None:
                    if self.count_adjacent(x, y, Acre.TREE) >= 3:
                        acre = Acre.TREE
                elif acre == Acre.TREE:
                    if self.count_adjacent(x, y, Acre.LUMBERYARD) >= 3:
                        acre = Acre.LUMBERYARD
                elif acre == Acre.LUMBERYARD:
                    if self.count_adjacent(x, y, Acre.LUMBERYARD) == 0 or self.count_adjacent(x, y, Acre.TREE) == 0:
                        acre = None

                new_map[(x, y)] = acre
        
        self.map = new_map
        self.minute += 1


    def run(self, minutes):
        while self.minute < minutes:
            self.process()


    def count(self, acre):
        """
        >>> forest = Forest("|#.\\n##|\\n.##\\n")
        >>> forest.count(Acre.TREE)
        2
        >>> forest.count(Acre.LUMBERYARD)
        5
        """

        return sum(1 for cell in self.map.values() if cell == acre)


    def resource_value(self):
        """
        >>> forest = Forest(".#.#...|#.\\n.....#|##|\\n.|..|...#.\\n..|#.....#\\n#.#|||#|#|\\n...#.||...\\n.|....|...\\n||...#|.#|\\n|.||||..|.\\n...#.|..|.")
        >>> forest.run(10)
        >>> forest.resource_value()
        1147
        """
        return self.count(Acre.TREE) * self.count(Acre.LUMBERYARD)


    def __str__(self):
        output = []

        for y in range(0, self.height):
            row = []
            units = []

            for x in range(0, self.width):
                acre = self.get(x, y)

                if acre is None:
                    row.append('.')
                else:
                    row.append(acre.value)

            output.append("".join(row) + " " + " ".join(units))


        return "\n".join(output)



def part1(data):
    """
    >>> part1(read_input())
    645946
    """

    forest = Forest(data)
    forest.run(10)
    return forest.resource_value()


def part2(data):
    """
    >>> part2(read_input())
    227688
    """

    forest = Forest(data)
    seen = set()
    start = None

    while True:
        map = str(forest)

        if map in seen:

            if start == None:
                start = forest.minute
                seen = set()
                seen.add(map)
            else:
                end = forest.minute
                loop = end - start
                delta = (1000000000 - start) % loop
                forest.run(end + delta)
                return forest.resource_value()

        seen.add(map)
        forest.process()


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
