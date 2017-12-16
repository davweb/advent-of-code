import itertools 
from collections import defaultdict
import re
import advent

PATTERN = re.compile(r"(\d+) <-> ((\d+, )*\d+)")

def read_input():
    return file('day16-input.txt').read().split(',')

def part1(data):
    for line in data:
        result = PATTERN.match(line)

def part2(data):
    pass

def main():
    part1("sample data")
    data = read_input()
    part1(data)
    part2(data)

if __name__ == "__main__":
    main()
