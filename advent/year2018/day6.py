#!/usr/local/bin/python3

import itertools
import sys
from collections import defaultdict

def read_input():
    file = open("input/2018/day6-input.txt", "r")    
    points = []

    for line in file.readlines():
        (x,y) = line.split(",")[:2]
        points.append((int(x), int(y)))

    return points

def taxicab_distance(a, b):
    """Calculate Manhattan distance

    >>> taxicab_distance((0, 0), (0, 0))
    0
    >>> taxicab_distance((0, 0), (1, 1))
    2
    >>> taxicab_distance((-1, -1), (-4, -3))
    5
    """

    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def bounds(points):
    """
    >>> bounds([(0, 0)])
    ((0, 0), (0, 0))
    >>> bounds([(7, 1), (-1, 9)])
    ((-1, 1), (7, 9))
    """

    left = min(x for (x,y) in points)
    right = max(x for (x,y) in points)
    top = min(y for (x,y) in points)
    bottom = max(y for (x,y) in points)
    
    return ((left, top), (right, bottom))

def part1(points):
    """
    >>> part1(read_input())
    4171
    """

    ((left, top), (right, bottom)) = bounds(points)

    areas = defaultdict(int)
    exclusions = set()

    for i in itertools.product(range(left, right + 1), range(top, bottom + 1)):    
        closest_distance = bottom + right

        for point in points:
            distance = taxicab_distance(i, point)

            if closest_distance > distance:
                closest_distance = distance
                closest_point = point
                closest_count = 1
            elif closest_distance == distance:
                closest_count += 1

        if closest_count == 1:
            areas[closest_point] += 1
            (x,y) = i

            # if a point is closest to another point on the border its area will be unbounded
            if x == left or x == right or y == top or y == bottom:
                exclusions.add(closest_point)

    return max(areas[point] for point in points if point not in exclusions)

def part2(points, progress=False):
    """What is the size of the region containing all locations which have a total
    distance to all given coordinates of less than 10000?
    
    >>> part2(read_input())
    39545
    """

    ((left, top), (right, bottom)) = bounds(points)

    max_distance = 10000
    area = 0
    count = 0
    
    # Even if all points are in same place no point checking further away than this distance
    limit = max_distance // len(points)

    # factor to calculate percentage complete
    pc = ((2 * limit + right - left) * (2 * limit + bottom - top)) / 100
    increment = pc // 100

    for i in itertools.product(range(left - limit, right + limit), range(top - limit, bottom + limit)):
        if progress:
            count += 1
            
            if count % increment == 0:
                print("{:3.0f}%".format(count / pc), end="\r", file=sys.stderr)

        distance = 0

        for point in points:
            distance += taxicab_distance(i, point)
            if distance >= max_distance:
                break

        if distance < max_distance:
            area += 1

    if progress:
        print("Done!", file=sys.stderr)

    return area

def main():
    data = read_input()
    print(part1(data))
    print(part2(data), progress=True)

if __name__ == "__main__":
    main()
