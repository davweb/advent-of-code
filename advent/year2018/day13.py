#!/usr/local/bin/python3

from collections import defaultdict
import itertools 
from functools import total_ordering
from enum import Enum

class Direction(Enum):
    UP  = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

@total_ordering
class Cart:

    VELOCITY = {
        Direction.UP: (0, -1),
        Direction.RIGHT: (1, 0),
        Direction.DOWN: (0, 1),
        Direction.LEFT: (-1, 0)
    }

    DIRECTION_MAP = {
        "^": Direction.UP,
        ">": Direction.RIGHT,
        "v": Direction.DOWN,
        "<": Direction.LEFT
    }

    TURNS = [3, 0, 1]

    def __init__(self, position, direction, tunnels):
        """
        >>> Cart((1, 2), "^", [])
        Cart(position=(1, 2), direction=Direction.UP, turn=0)
        >>> Cart((-1, 7), "v", [])
        Cart(position=(-1, 7), direction=Direction.DOWN, turn=0)
        >>> Cart((0 , 0), "<", [])
        Cart(position=(0, 0), direction=Direction.LEFT, turn=0)
        >>> Cart((99, 99), ">", [])
        Cart(position=(99, 99), direction=Direction.RIGHT, turn=0)
        >>> Cart((3, 2), "a", [])
        Traceback (most recent call last):
        ...
        ValueError: Invalid direction 'a'
        """

        self.position = position
        self.tunnels = tunnels
        self.turn = 0
    
        try:
            self.direction = Cart.DIRECTION_MAP[direction]
        except KeyError:
            raise ValueError("Invalid direction '{}'".format(direction))
    
    def __repr__(self):
        return "Cart(position={position}, direction={direction}, turn={turn})".format(**self.__dict__)

    def __lt__(self, other):
        return self.position[::-1] < other.position[::-1]

    def __eq__(self, other):
        return self.position == other.position

    def move(self):
        r"""
        >>> Cart((0,0), ">", ['-','-']).move()
        Cart(position=(1, 0), direction=Direction.RIGHT, turn=0)
        >>> Cart((1,0), "<", ['/','-']).move()
        Cart(position=(0, 0), direction=Direction.DOWN, turn=0)
        >>> map = []
        >>> map.append(['|', '\\'])
        >>> Cart((0,0), "v", map).move()
        Cart(position=(0, 1), direction=Direction.RIGHT, turn=0)
        >>> map = []
        >>> map.append(['-', '-', '-'])
        >>> map.append(['+', '+', '+'])
        >>> c = Cart((0,2), ">", map)
        >>> c.move()
        Cart(position=(1, 2), direction=Direction.UP, turn=1)
        >>> c.move()
        Cart(position=(1, 1), direction=Direction.UP, turn=2)
        >>> c.move()
        Cart(position=(1, 0), direction=Direction.RIGHT, turn=0)
        """

        velocity = Cart.VELOCITY[self.direction]
        self.position = tuple(p + v for p, v in zip(self.position, velocity))

        cell = self.tunnels[self.position[0]][self.position[1]]

        if cell == "/":
            if self.direction == Direction.UP:
                self.direction = Direction.RIGHT 
            elif self.direction == Direction.DOWN:
                self.direction = Direction.LEFT 
            elif self.direction == Direction.LEFT:
                self.direction = Direction.DOWN 
            elif self.direction == Direction.RIGHT:
                self.direction = Direction.UP 
        elif cell == "\\":
            if self.direction == Direction.UP:
                self.direction = Direction.LEFT 
            elif self.direction == Direction.DOWN:
                self.direction = Direction.RIGHT 
            elif self.direction == Direction.LEFT:
                self.direction = Direction.UP 
            elif self.direction == Direction.RIGHT:
                self.direction = Direction.DOWN 
        elif cell == "+":
            self.direction = Direction((self.direction.value + Cart.TURNS[self.turn]) % 4)
            self.turn = (self.turn + 1) % 3

        return self
        

def read_input():
    with open('input/2018/day13-input.txt', 'r') as file:
        data = [[cell for cell in line] for line in file.readlines()]
        
    # Swap x and y before returning
    return list(zip(*data))

def print_map(map):
    for y in range(0, len(map[0])):
        row = ''
        for x in range(0, len(map)):
            row += map[x][y]

        print(row)


def get_carts(tunnels):
    carts = []

    for (x,y) in itertools.product(range(0, len(tunnels)), range(0, len(tunnels[0]))):
        cell = tunnels[x][y]

        if cell == "^" or cell == "v":
            tunnels[x][y] == "|"
        elif cell == "<" or cell == ">":
            tunnels[x][y] == "-"
        else:
            continue

        carts.append(Cart((x,y), cell, tunnels))

    return carts


def part1(tunnels):
    """
    >>> part1(read_input())
    (117, 62)
    """

    carts = get_carts(tunnels)
    positions = set(cart.position for cart in carts)

    while True:
        carts.sort()

        for cart in carts:
            positions.remove(cart.position)
            cart.move()
            
            if cart.position in positions:
                return cart.position
            
            positions.add(cart.position)


def part2(tunnels):
    """
    >>> part2(read_input())
    (69, 67)
    """

    carts = get_carts(tunnels)
    positions = set(cart.position for cart in carts)
    
    while True:
        carts.sort()
        crashed = []
        
        for cart in carts:
            if cart in crashed:
                continue 

            positions.remove(cart.position)
            cart.move()
            
            if cart.position in positions:
                crashed += [other for other in carts if other.position == cart.position]    
                positions.remove(cart.position)
            else:
                positions.add(cart.position)

        carts = [cart for cart in carts if cart not in crashed]

        if len(carts) == 1:
            return carts[0].position


def main():
    map = read_input()
    print(part1(map))
    print(part2(map))


if __name__ == "__main__":
    main()
