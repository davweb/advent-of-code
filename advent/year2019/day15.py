#!/usr/local/bin/python3

from collections import defaultdict
import enum
from advent.year2019.intcode import IntCode
from advent import bounds
import sys

def read_input():
    return [int(code) for code in open('input/2019/day15-input.txt', 'r').read().split(',')]

class Movement(enum.Enum):

    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, forward, back, x, y):
        self.forward = forward
        self.back = back
        self.x = x
        self.y = y

    NORTH = 1, 2, 0, 1
    SOUTH = 2, 1, 0, -1
    WEST = 3, 4, -1, 0
    EAST = 4, 3, 1, 0
    

def explore(code):
    i = IntCode(code)
    location = (0, 0)
    seen = {}
    seen[location] = "S"

    def search(location):

        for movement in Movement:
            next_location = (location[0] + movement.x, location[1] + movement.y)
            
            if next_location in seen: 
                continue

            output = i.execute([movement.forward])

            if output == 0:
                seen[next_location] = '#'
            elif output == 1:
                seen[next_location] = ' '
                search(next_location)
                i.execute([movement.back])
            elif output == 2:
                seen[next_location] = '*'
                search(next_location)
                i.execute([movement.back])

    search(location)
    return seen

def draw_map(robot_map):
    (left, top), (right, bottom) = bounds(robot_map.keys())
    output = []

    for y in range(top, bottom + 1):
        line = []

        for x in range(left, right + 1):
            if (x,y) in robot_map:
                line.append(robot_map[(x, y)])
            else:
                line.append("?")

        output.append("".join(line))

    return "\n".join(output)


def part1(robot_map):
    """
    >>> part1(explore(read_input()))
    262
    """

    nodes = [key for key in robot_map.keys() if robot_map[key] != '#']
    destination = next(node for node in nodes if robot_map[node] == '*')

    distances = defaultdict(lambda: 999)
    distances[(0,0)] = 0

    while nodes[0] != destination:
        nodes.sort(key=lambda node: distances[node])
        location = nodes[0]
        distance = distances[location] + 1
        neighbours = [node for node in nodes if abs(node[0] - location[0]) + abs(node[1] - location[1]) == 1]

        for neighbour in neighbours:
            if distances[neighbour] > distance:
                distances[neighbour] = distance

        nodes.remove(location)

    return distances[destination]

def part2(robot_map):
    """
    >>> part2(explore(read_input()))
    314
    """

    nodes = [key for key in robot_map.keys() if robot_map[key] != '#']
    start = next(node for node in nodes if robot_map[node] == '*')
    queue = [(start, 0)]
    max_distance = 0
    seen = set()

    while queue:
        (location, distance) = queue.pop(0)
        seen.add(location)
        if distance > max_distance:
            max_distance = distance

        neighbours = [node for node in nodes if abs(node[0] - location[0]) + abs(node[1] - location[1]) == 1]

        for neighbour in neighbours:
            if neighbour not in seen:
                queue.append((neighbour, distance + 1))

    return max_distance


def main():
    code = read_input()
    robot_map = explore(code)
    print(draw_map(robot_map))
    print(part1(robot_map))
    print(part2(robot_map))

if __name__ == "__main__":
    main()
