from enum import Enum

class Seat(Enum):
    UNOCCUPIED = 'L'
    OCCUPIED = '#'


def read_input():
    file = open('input/2020/day11-input.txt', 'r')
    return file.read()


class Floor:
    def __init__(self, text):
        self.turn = 0
        self.map = {}

        x = 0
        y = 0

        for y, row in enumerate(text.strip().split("\n")):
            for x, cell in enumerate(row):
                if cell == Seat.UNOCCUPIED.value:
                    acre = Seat.UNOCCUPIED
                elif cell == Seat.OCCUPIED.value:
                    acre = Seat.OCCUPIED
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
    
    
    def count_adjacent(self, cell_x, cell_y, seat):
        """
        >>> floor = Floor("L#.\\n##L\\n.##\\n")
        >>> floor.count_adjacent(1, 1, Seat.UNOCCUPIED)
        2
        >>> floor.count_adjacent(1, 1, Seat.OCCUPIED)
        4
        """

        return sum(1 for (x, y) in self.adjacent_cells(cell_x, cell_y) if self.get(x, y) == seat)

    def visible_seats(self, start_x, start_y):
        visible = []

        for dx, dy in ((-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)):
            x = start_x + dx
            y = start_y + dy

            while 0 <= x <= self.width and 0 <= y <= self.height:
                cell = self.get(x, y)
                
                if cell is not None:
                    visible.append(cell)
                    break

                x += dx
                y += dy

        return visible


    def count_visible(self, cell_x, cell_y, seat):
        return sum(1 for s in self.visible_seats(cell_x, cell_y) if s == seat)


    def all_seats(self):
        return self.map.items()


    def process(self):
        new_map = {}
        changes = 0

        for ((x, y), cell) in self.all_seats():

            if cell == Seat.UNOCCUPIED:
                if self.count_adjacent(x, y, Seat.OCCUPIED) == 0:
                    cell = Seat.OCCUPIED
                    changes += 1
            elif cell == Seat.OCCUPIED:
                if self.count_adjacent(x, y, Seat.OCCUPIED) >= 4:
                    cell = Seat.UNOCCUPIED
                    changes += 1

            new_map[(x, y)] = cell
        
        self.map = new_map
        self.turn += 1
        return changes


    def run(self):
        """
        >>> floor = Floor("L.LL.LL.LL\\nLLLLLLL.LL\\nL.L.L..L..\\nLLLL.LL.LL\\nL.LL.LL.LL\\nL.LLLLL.LL\\n..L.L.....\\nLLLLLLLLLL\\nL.LLLLLL.L\\nL.LLLLL.LL") 
        >>> floor.run()
        37
        """
        
        while self.process() > 0:
            pass

        return self.count(Seat.OCCUPIED)


    def process_visible(self):
        new_map = {}
        changes = 0

        for ((x, y), cell) in self.all_seats():

            if cell == Seat.UNOCCUPIED:
                if self.count_visible(x, y, Seat.OCCUPIED) == 0:
                    cell = Seat.OCCUPIED
                    changes += 1
            elif cell == Seat.OCCUPIED:
                if self.count_visible(x, y, Seat.OCCUPIED) >= 5:
                    cell = Seat.UNOCCUPIED
                    changes += 1

            new_map[(x, y)] = cell
        
        self.map = new_map
        self.turn += 1
        return changes


    def run_visible(self):
        """
        >>> floor = Floor("L.LL.LL.LL\\nLLLLLLL.LL\\nL.L.L..L..\\nLLLL.LL.LL\\nL.LL.LL.LL\\nL.LLLLL.LL\\n..L.L.....\\nLLLLLLLLLL\\nL.LLLLLL.L\\nL.LLLLL.LL") 
        >>> floor.run_visible()
        26
        """
        
        while self.process_visible() > 0:
            pass

        return self.count(Seat.OCCUPIED)


    def count(self, acre):
        """
        >>> floor = Floor("L#.\\n##L\\n.##\\n")
        >>> floor.count(Seat.UNOCCUPIED)
        2
        >>> floor.count(Seat.OCCUPIED)
        5
        """

        return sum(1 for cell in self.map.values() if cell == acre)


    def __str__(self):
        output = []

        for y in range(0, self.height):
            row = []
            units = []

            for x in range(0, self.width):
                cell = self.get(x, y)

                if cell is None:
                    row.append('.')
                else:
                    row.append(cell.value)

            output.append("".join(row) + " " + " ".join(units))


        return "\n".join(output)


def part1(data):
    """
    >>> part1(read_input())
    2406
    """

    floor = Floor(data)
    floor.run()
    return floor.count(Seat.OCCUPIED)


def part2(data):
    """
    >>> part2(read_input())
    2149
    """

    floor = Floor(data)
    floor.run_visible()
    return floor.count(Seat.OCCUPIED)


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
