#!/usr/local/bin/python3

from collections import defaultdict

def read_input():
    file = open("input/2019/day6-input.txt", "r")    
    orbits = []

    for line in file.readlines():
        (x,y) = line.strip().split(")")[:2]
        orbits.append((x,y))

    return orbits

def count_orbits(point, relationships):
    count = 0
    super_orbits = relationships[point]

    for s in super_orbits:
        count += 1 + count_orbits(s, relationships)

    return count

def part1(orbits):
    """
    >>> part1(read_input())
    110190
    """

    relationships  = defaultdict(list)
    points = set()

    for (left, right) in orbits:
       points.add(left)
       points.add(right)
       relationships[right].append(left)
    
    count = 0

    for point in points:
        count += count_orbits(point, relationships)

    return count

def part2(orbits):
    """
    >>> part2(read_input())
    343
    """

    relationships  = defaultdict(list)

    for (left, right) in orbits:
        relationships[left].append(right)
        relationships[right].append(left)

    start = 'YOU'
    end = 'SAN'
    
    seen = set()
    queue = [[start]]

    while queue:
        route = queue.pop()
        q = route[-1]
        seen.add(q)

        if q == end:
            # Number of transfers doesn't include YOU, SAN or first element in route
            return len(route) - 3
            
        for n in relationships[q]:
            if n not in seen:
                new_route = route + [n]
                queue.append(new_route)

    raise Exception("Failed to find {}".format(end))

def main():
    data = read_input() 
    print(part1(data))
    print(part2(data))

if __name__ == "__main__":
    main()
