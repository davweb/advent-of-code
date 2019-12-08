#!/usr/local/bin/python3

def read_input():
    file = open('input/day1-input.txt', 'r')
    return [int(line) for line in file.readlines()]

def calculate_fuel(mass):
    """Calculate the fuel required for a module

    >>> calculate_fuel(12)
    2
    >>> calculate_fuel(14)
    2
    >>> calculate_fuel(1969)
    654
    >>> calculate_fuel(100756)
    33583
    """

    return mass // 3 - 2

def calculate_all_fuel(mass):
    """So, for each module mass, calculate its fuel and add it to the total. Then, treat the fuel amount you just calculated as the input mass and repeat the process, continuing until a fuel requirement is zero or negative.

    >>> calculate_all_fuel(14)
    2
    >>> calculate_all_fuel(1969)
    966
    >>> calculate_all_fuel(100756)
    50346
    """

    total_fuel = 0
    fuel = calculate_fuel(mass)

    while fuel > 0:
        total_fuel += fuel
        fuel = calculate_fuel(fuel)

    return total_fuel

def part1(data):
    """
    >>> part1(read_input())
    3471229
    """
    return sum(calculate_fuel(mass) for mass in data)

def part2(data):
    """
    >>> part2(read_input())
    5203967
    """
    return sum(calculate_all_fuel(mass) for mass in data)

def main():
    data = read_input()
    print(part1(data))
    print(part2(data))

if __name__ == "__main__":
    main()
