# -*- coding: utf-8 -*-

import itertools
from collections import deque

MICROCHIP = 1
GENERATOR = 2


class Chip:
    elements = []

    def __init__(self, kind, element):
        self.kind = kind

        if element not in Chip.elements:
            Chip.elements.append(element)

        self.element_id = Chip.elements.index(element)
        self.hash = self.kind + self.element_id * 3

    def __eq__(self, other):
        return self.kind == other.kind and self.element_id == other.element_id

    def __hash__(self):
        return self.hash

    def __repr__(self):
        return f'Chip({self.kind}, {Chip.elements[self.element_id]})'

    def __lt__(self, other):
        if self.kind == other.kind:
            return self.element_id < other.element_id
        else:
            return self.kind < other.kind


class Building:
    def __init__(self):
        self.floors = [(), (), (), ()]
        self.elevator = 0
        self.__rehash()

    def copy(self):
        other = Building()
        other.elevator = self.elevator

        for i in range(4):
            other.floors[i] = self.floors[i]

        return other

    def add(self, floor, *chips):
        self.floors[floor] = tuple(sorted(self.floors[floor] + chips))
        self.__rehash()

    def move(self, old_floor, new_floor, *chips):
        self.floors[old_floor] = tuple(sorted(x for x in self.floors[old_floor] if x not in chips))
        self.add(new_floor, *chips)

    def moves(self):
        """
        >>> b = Building()
        >>> b.elevator = 1
        >>> b.add(1, Chip(MICROCHIP, 'gold'))
        >>> b.add(1, Chip(GENERATOR, 'gold'))
        >>> b.add(1, Chip(GENERATOR, 'silver'))
        >>> len(b.moves())
        4
        """

        possible_moves = []

        new_floors = []

        if self.elevator < 3:
            new_floors.append(self.elevator + 1)

        # No point moving down if all the floors below are empty
        if self.elevator > 0 and  any(other_floor != () for other_floor in self.floors[0:self.elevator]):
            new_floors.append(self.elevator - 1)

        passengers = [(chip,) for chip in self.floors[self.elevator]]

         # You can't get in a position where an illegal pair in the lift leads to a valid state
        passengers += list(itertools.combinations(self.floors[self.elevator], 2))

        for new_floor in new_floors:
            for chips in passengers:
                new_building = self.copy()
                new_building.elevator = new_floor

                new_building.move(self.elevator, new_floor, *chips)

                if new_building.is_valid():
                    possible_moves.append(new_building)

        return possible_moves


    def is_valid(self):
        """
        >>> b = Building()
        >>> b.add(0, Chip(MICROCHIP, 'gold'))
        >>> b.is_valid()
        True
        >>> b.add(0, Chip(GENERATOR, 'silver'))
        >>> b.is_valid()
        False
        >>> b.add(0, Chip(GENERATOR, 'gold'))
        >>> b.is_valid()
        True
        """

        for floor in self.floors:
            if len(floor) < 2:
                continue

            generators = [chip.element_id for chip in floor if chip.kind == GENERATOR]

            if generators and any (chip.kind == MICROCHIP and chip.element_id not in generators for chip in floor):
                return False

        return True


    def finished(self):
        """
        >>> b = Building()
        >>> b.finished()
        True
        >>> b.add(3, Chip(MICROCHIP, 'gold'))
        >>> b.finished()
        True
        >>> b.add(0, Chip(GENERATOR, 'silver'))
        >>> b.finished()
        False
        """

        return self.floors[0] == () and self.floors[1] == () and self.floors[2] == ()

    def __eq__(self, other):
        """
        >>> a = Building()
        >>> a.add(0, Chip(MICROCHIP, 'gold'))
        >>> b = Building()
        >>> a == b
        False
        >>> b.add(0, Chip(MICROCHIP, 'gold'))
        >>> a == b
        True
        """

        # return self.elevator == other.elevator and all(a == b for a, b in zip(self.floors, other.floors))
        return self.elevator == other.elevator \
            and self.floors[0] == other.floors[0] \
            and self.floors[1] == other.floors[1] \
            and self.floors[2] == other.floors[2] \
            and self.floors[3] == other.floors[3]

    def __rehash(self):
        self.hash = hash((self.elevator, *self.floors))

    def __hash__(self):
        return self.hash


def shortest_route(b):
    """
    >>> b = Building()
    >>> b.add(0, Chip(MICROCHIP, 'H'))
    >>> b.add(0, Chip(MICROCHIP, 'L'))
    >>> b.add(1, Chip(GENERATOR, 'H'))
    >>> b.add(2, Chip(GENERATOR, 'L'))
    >>> shortest_route(b)
    11
    """

    shortest = None
    queue = deque([(b, 0)])
    seen = {}

    while queue:
        (building, distance) = queue.popleft()

        if building in seen:
            best = seen[building]
            if best <= distance:
                continue

        seen[building] = distance

        if shortest is not None and shortest <= distance:
            continue

        if building.finished():
            shortest = distance
            continue

        for move in building.moves():
            queue.append((move, distance + 1))

    return shortest


def setup():
    b = Building()
    b.add(0, Chip(GENERATOR, 'polonium'))
    b.add(0, Chip(GENERATOR, 'thulium'))
    b.add(0, Chip(MICROCHIP, 'thulium'))
    b.add(0, Chip(GENERATOR, 'promethium'))
    b.add(0, Chip(GENERATOR, 'ruthenium'))
    b.add(0, Chip(MICROCHIP, 'ruthenium'))
    b.add(0, Chip(GENERATOR, 'cobalt'))
    b.add(0, Chip(MICROCHIP, 'cobalt'))

    b.add(1, Chip(MICROCHIP, 'polonium'))
    b.add(1, Chip(MICROCHIP, 'promethium'))

    return b


def part1():
    """
    >>> part1()
    47
    """

    return shortest_route(setup())


def part2():
    """
    # >>> part2()
    71
    """

    b = setup()

    b.add(0, Chip(GENERATOR, 'elerium'))
    b.add(0, Chip(MICROCHIP, 'elerium'))
    b.add(0, Chip(GENERATOR, 'dilithium'))
    b.add(0, Chip(MICROCHIP, 'dilithium'))

    return shortest_route(b)


def main():
    print(part1())
    print(part2())

if __name__ == "__main__":
    main()
