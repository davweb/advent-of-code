#!/usr/local/bin/python3

from collections import defaultdict
from itertools import product
from functools import lru_cache


@lru_cache(maxsize=None)
def calc_power(serial_number, x, y):
    """
    Find the fuel cell's rack ID, which is its X coordinate plus 10.
    Begin with a power level of the rack ID times the Y coordinate.
    Increase the power level by the value of the grid serial number (your puzzle input).
    Set the power level to itself multiplied by the rack ID.
    Keep only the hundreds digit of the power level (so 12345 becomes 3; numbers with no hundreds digit become 0).
    Subtract 5 from the power level.
    
    >>> calc_power(8, 3, 5)
    4
    >>> calc_power(57, 122, 79)
    -5
    >>> calc_power(39, 217, 196)
    0
    >>> calc_power(71, 101, 153)
    4
    """

    rack_id = x + 10
    power = rack_id * y
    power += serial_number
    power *= rack_id
    power = power // 100 % 10
    power -= 5
    return power

@lru_cache(maxsize=None)
def calc_grid_power(serial_number, cell, size):
    """
    >>> calc_grid_power(18, (33, 45), 3)
    29
    >>> calc_grid_power(42, (21, 61), 3)
    30
    >>> calc_grid_power(18, (90, 269), 16)
    113
    >>> calc_grid_power(42, (232, 251), 12)
    119
    """
    
    (x, y) = cell

    if size == 1:
        power = calc_power(serial_number, x, y)
    elif size % 2 == 0:
        half = size // 2
        power = calc_grid_power(serial_number, (x, y), half) 
        power += calc_grid_power(serial_number, (x + half, y), half) 
        power += calc_grid_power(serial_number, (x, y + half), half) 
        power += calc_grid_power(serial_number, (x + half, y + half), half)
    elif size % 3 == 0:
        third = size // 3
        power = calc_grid_power(serial_number, (x, y), third)
        power += calc_grid_power(serial_number, (x + third, y), third)
        power += calc_grid_power(serial_number, (x + 2 * third, y), third) 
        power += calc_grid_power(serial_number, (x, y + third), third) 
        power += calc_grid_power(serial_number, (x, y + 2 * third), third) 
        power += calc_grid_power(serial_number, (x + third, y + third), third * 2) 
    else:
        power = calc_grid_power(serial_number, (x, y), size - 1) 
        power += sum(calc_power(serial_number, x + dx, y + size - 1) for dx in range(0, size - 1))
        power += sum(calc_power(serial_number, x + size - 1, y + dy) for dy in range(0, size))
            
    return power

def part1(serial_number):
    """
    >>> part1(9005)
    (20, 32)
    """

    # minimum possible power is -5 * 9 
    max_power = -46
    
    for cell in product(range(1, 299), range(1, 299)):
        grid_power = calc_grid_power(serial_number, cell, 3)
        if max_power < grid_power:
            max_power = grid_power
            max_cell = cell

    return (max_cell)

def part2(serial_number, progress=False):
    # power will be at least -5 since it's the minimum power for a 1 * 1 square
    max_power = -6
    
    for size in range(1, 301):
        if progress:
            print("{:3.0f}%".format(size / 3 ), end = "\r") 

        for cell in product(range(1, 302 - size), range(1, 302 - size)):
            grid_power = calc_grid_power(serial_number, cell, size)

            if max_power < grid_power:
                max_power = grid_power
                max_cell = cell
                max_size = size

    return (max_cell) + (max_size,)

def main():
    # Serial number is 9005
    print(part1(9005))
    print(part2(9005), True)

if __name__ == "__main__":
    main()
    