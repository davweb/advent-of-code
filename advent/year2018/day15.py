#!/usr/local/bin/python3

def read_input():
    file = open('input/2018/day15-input.txt', 'r')
    return file.read()


class Unit:
    
    def __init__(self, elf, ap):
        self.elf = elf
        self.hp = 200
        self.ap = ap

    def __str__(self):
        return 'E' if self.elf else 'G'

    def __repr__(self):
        return 'Unit({elf}, {hp})'.format(**self.__dict__)    


class Location:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __lt__(self, other):
        return self.y < other.y or (self.y == other.y and self.x < other.x)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return '({x}, {y})'.format(**self.__dict__)

    def __repr__(self):
        return 'Location({x}, {y})'.format(**self.__dict__)    


def join_locations(locations):
    return ", ".join(str(location) for location in locations)


class Board:

    def __init__(self, text, elf_ap=3):
        self.board = {}
        self.turns = 0
        self.dead_elves = 0

        x = 0
        y = 0

        for y, row in enumerate(text.split("\n")):
            for x, cell in enumerate(row):
                if cell == 'E':
                    value = Unit(True, elf_ap)
                elif cell == 'G':
                    value = Unit(False, 3)
                elif cell == '#':
                    value = '#'
                elif cell == '.':
                    value = None
                else:
                    raise ValueError("Invalid Board cell '{}'".format(cell))

                self.board[Location(x,y)] = value
          
        self.width = x + 1
        self.height = y + 1

    def __str__(self):
        output = []

        output.append("Turn {}".format(self.turns))
        output.append("")

        for y in range(0, self.height):
            row = []
            units = []

            for x in range(0, self.width):
                cell = self[Location(x, y)]

                if type(cell) == Unit:
                    char = 'E' if cell.elf else 'G'
                    row.append(char)
                    units.append('{}({})'.format(char, cell.hp))
                elif cell is None:
                    row.append('.')
                else:
                    row.append(cell)

            output.append("".join(row) + " " + " ".join(units))

        output.append("")
        output.append("HP {} - Score {} - Dead Elves {}".format(self.total_hp(), self.score(), self.dead_elves))

        return "\n".join(output)


    def __getitem__(self, key):
        return self.board.get(key, None)


    def __setitem__(self, key, value):
        self.board[key] = value


    def filled_locations(self):
        return self.board.keys()


    def targets(self, location):
        """
        >>> board = Board("#######\\n#E..G.#\\n#...#.#\\n#.G.#G#\\n#######")
        >>> join_locations(board.targets(Location(1,1)))
        '(4, 1), (2, 3), (5, 3)'
        """

        source = self[location]
        find_elf = not source.elf 

        targets = []

        for location in self.filled_locations():
            value = self[location]

            if type(value) == Unit and value.elf == find_elf:
                targets.append(location)

        return targets

 
    def adjacents(self, location):
        """
        Return the other locations adjacent to pass in location in reading order

        >>> board = Board("...\\n...\\n...")
        >>> join_locations(board.adjacents(Location(0, 0)))
        '(1, 0), (0, 1)'
        >>> join_locations(board.adjacents(Location(1, 1)))
        '(1, 0), (0, 1), (2, 1), (1, 2)'
        >>> join_locations(board.adjacents(Location(2, 2)))
        '(2, 1), (1, 2)'
        """
        
        x = location.x
        y = location.y
        
        adjacents = []

        if y > 0:
            adjacents.append(Location(x, y - 1))
            
        if x > 0:
            adjacents.append(Location(x - 1, y))

        if x < self.width - 1:
            adjacents.append(Location(x + 1, y))
        
        if y < self.height - 1:
            adjacents.append(Location(x, y + 1))

        return adjacents


    def empty_adjacents(self, location):
        return [a for a in self.adjacents(location) if self[a] is None]


    def find_path(self, source, destination):
        """
        >>> board = Board("#######\\n#E..G.#\\n#...#.#\\n#.G.#G#\\n#######")
        >>> board.find_path(Location(1,1), Location(3,3))
        (3, Location(2, 1))
        >>> board.find_path(Location(1,1), Location(1,2))
        (0, Location(1, 2))
        """

        # Work out distances from the destination to every other square
        paths = {}
        paths[destination] = 0
        queue = [destination]

        while queue:
            location = queue.pop(0)
            option_score = paths[location] + 1

            for option in self.empty_adjacents(location):
                if option not in paths or paths[option] > option_score:
                    paths[option] = option_score
                    queue.append(option)

        # Work out which step brings us closest (in reading order)  
        shortest_distance = None
        first_step = None

        for step in self.empty_adjacents(source):
            if step not in paths:
                continue
            step_distance = paths[step]

            if shortest_distance is None or step_distance < shortest_distance:
                shortest_distance = step_distance
                first_step = step

        return (shortest_distance, first_step)


    def unit_locations(self):
        """
        >>> board = Board('#######\\n#.G.E.#\\n#E.G.E#\\n#.G.E.#\\n#######')
        >>> units = board.unit_locations()
        >>> ", ".join(str(unit) for unit in units)
        '(2, 1), (4, 1), (1, 2), (3, 2), (5, 2), (2, 3), (4, 3)'
        """

        return sorted(l for l in self.filled_locations() if type(self[l]) == Unit)


    def take_turn(self):
        unit_locations = self.unit_locations()

        for location in unit_locations:
            unit = self[location]

            # Skip killed units
            if unit is None:
                continue

            enemy = not unit.elf
            adjacents = self.adjacents(location)
            targets = self.targets(location)

            # If there are no targets the battle is over 
            if not targets:
                self.running = False
                return

            # only move if not next to a target
            if not set(adjacents).intersection(set(targets)):

                # remove surrounded targets
                targets = (t for t in targets if len(self.empty_adjacents(t)) != 0)

                moves = (self.find_path(location, target) for target in targets)
                moves = sorted(move for move in moves if move[0] is not None)

                if moves:
                    distance, step = moves[0]

                    if (distance > 0):
                        self[step] = unit
                        self[location] = None
                        location = step

            # attack if we can
            attack_target = None
            attack_location = None

            for adjacent in self.adjacents(location):
                neighbour = self[adjacent]

                if type(neighbour) == Unit and neighbour.elf == enemy:
                    if attack_target is None or attack_target.hp > neighbour.hp:
                        attack_target = neighbour
                        attack_location = adjacent

            if attack_target:
                attack_target.hp -= unit.ap

                if attack_target.hp <= 0:
                    self[attack_location] = None
                    if attack_target.elf:
                        self.dead_elves += 1

        self.turns += 1


    def play(self, debug=False):
        """
        >>> board = Board("#######\\n#.G...#\\n#...EG#\\n#.#.#G#\\n#..G#E#\\n#.....#\\n#######")
        >>> board.play()
        >>> board.score()
        27730
        >>> board = Board("#######\\n#G..#E#\\n#E#E.E#\\n#G.##.#\\n#...#E#\\n#...E.#\\n#######")
        >>> board.play()
        >>> board.score()
        36334
        >>> board = Board("#######\\n#E..EG#\\n#.#G.E#\\n#E.##E#\\n#G..#.#\\n#..E#.#\\n#######")
        >>> board.play()
        >>> board.score()
        39514
        >>> board = Board("#######\\n#E.G#.#\\n#.#G..#\\n#G.#.G#\\n#G..#.#\\n#...E.#\\n#######")
        >>> board.play()
        >>> board.score()
        27755
        >>> board = Board("#######\\n#.E...#\\n#.#..G#\\n#.###.#\\n#E#G#G#\\n#...#G#\\n#######")
        >>> board.play()
        >>> board.score()
        28944
        >>> board = Board("#########\\n#G......#\\n#.E.#...#\\n#..##..G#\\n#...##..#\\n#...#...#\\n#.G...G.#\\n#.....G.#\\n#########")
        >>> board.play()
        >>> board.score()
        18740
        >>> board = Board("#######\\n#.G...#\\n#...EG#\\n#.#.#G#\\n#..G#E#\\n#.....#\\n#######", 15)
        >>> board.play()
        >>> board.score()
        4988
        >>> board.dead_elves
        0
        >>> board = Board("#########\\n#G......#\\n#.E.#...#\\n#..##..G#\\n#...##..#\\n#...#...#\\n#.G...G.#\\n#.....G.#\\n#########", 34)
        >>> board.play()
        >>> board.score()
        1140
        >>> board.dead_elves
        0
        """

        self.running = True

        while self.running:  
            if debug:
                print(self)

            self.take_turn()

        if debug:
            print(self)


    def total_hp(self):
        return sum(self[unit_location].hp for unit_location in self.unit_locations())


    def score(self):
        return self.turns * self.total_hp()


def part1(data, debug=False):
    """
    >>> part1(read_input())
    184206
    """
    
    board = Board(data)
    board.play()
    return board.score()


def part2(data, debug=False):
    """
    >>> part2(read_input())
    41804
    """
    
    lower = 4
    upper = 50
    scores = {}

    while upper - lower > 1:
        middle = lower + (upper - lower) // 2

        board = Board(data, middle)
        board.play()
        scores[middle] = board.score()

        if board.dead_elves == 0:
            upper = middle
        else:
            lower = middle

    return scores[upper]


def main():
    data = read_input()

    print(part1(data))
    print(part2(data, True))


if __name__ == "__main__":
    main()
