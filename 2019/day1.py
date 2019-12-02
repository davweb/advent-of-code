#!usr/local/bin/python3

# Fuel required to launch a given module is based on its mass. Specifically, to
# find the fuel required for a module, take its mass, divide by three, round
# down, and subtract 2.
#
# For example:
#
# * For a mass of 12, divide by 3 and round down to get 4, then subtract 2 to
#   get 2.
# * For a mass of 14, dividing by 3 and rounding down still yields 4, so the
#   fuel required is also 2.
# * For a mass of 1969, the fuel required is 654.
# * For a mass of 100756, the fuel required is 33583.
# * The Fuel Counter-Upper needs to know the total fuel requirement. To find it,
#   individually calculate the fuel needed for the mass of each module (your
#   puzzle input), then add together all the fuel values.
#
# What is the sum of the fuel requirements for all of the modules on your
# spacecraft?

def read_input():
    file = open('day1-input.txt', 'r')
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
    total = sum(calculate_fuel(mass) for mass in data)
    print(total);

def part2(data):
    total = sum(calculate_all_fuel(mass) for mass in data)
    print(total);

def main():
    data = read_input()
    part1(data)
    part2(data)

if __name__ == "__main__":
    main()
