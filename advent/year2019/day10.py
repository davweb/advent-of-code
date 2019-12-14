#!/usr/local/bin/python3

import itertools
import math

def read_input():
    with open('input/2019/day10-input.txt', 'r') as file:
        data = [[cell == "#" for cell in line.strip()] for line in file.readlines()]
        return set((x,y) for (x,y) in itertools.product(range(0, len(data[0])), range(0,len(data))) if data[y][x])

def path(start, end):
    """
    >>> path((1,1), (1,1))
    []
    >>> path((0,0), (2,2))
    [(1, 1)]
    >>> path((1,2), (7,5))
    [(3, 3), (5, 4)]
    >>> path((9, 10), (6, 10))
    [(8, 10), (7, 10)]
    >>> path((10, 9), (10, 6))
    [(10, 8), (10, 7)]
    >>> path((1,1), (3,8))
    []
    >>> path((4, 2), (4, 4))
    [(4, 3)]
    """

    (x, y) = start
    (ex, ey) = end
    dx = ex - x 
    dy = ey - y
    path = []

    if dx == 0 and dy == 0:
        pass
    elif dy == 0 or (dx != 0 and abs(dx) < abs(dy)):
        r = range(1, dx) if dx > 0 else range(-1, dx, -1)

        for mx in r:
            my = dy * mx / dx
            if my.is_integer():
                my = int(my)
                path.append((x + mx, y + my))
    else:
        r = range(1, dy) if dy > 0 else range(-1, dy, -1)

        for my in r:
            mx = dx * my / dy

            if mx.is_integer():
                mx = int(mx)
                path.append((x + mx, y + my))

    return path

def can_see(asteroid, asteroids):
    """
    .7..7
    .....
    67775
    ....7
    ...87

    >>> asteroids = set(((1, 0), (4, 0), (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (4, 3), (3, 4), (4, 4)))
    >>> can_see((1,0), asteroids)
    [(1, 2), (3, 2), (4, 4), (2, 2), (4, 2), (0, 2), (4, 0)]
    >>> len(can_see((4,0), asteroids))
    7
    >>> len(can_see((0,2), asteroids))
    6
    >>> len(can_see((2,2), asteroids))
    7
    >>> len(can_see((4,2), asteroids))
    5
    >>> len(can_see((3,4), asteroids))
    8
    """

    visible = []

    for other in asteroids:
        if other == asteroid:
            continue
        if not next((step for step in path(asteroid, other) if step in asteroids), None):
            visible.append(other)

    return visible


def part1(asteroids):
    """
    >>> part1(read_input())
    314
    """
 
    return max(len(can_see(asteroid, asteroids)) for asteroid in asteroids)



def part2(asteroids):
    """
    >>> part2(read_input())
    1513
    """

    asteroids = asteroids.copy()
    max_seen = 0
    
    for asteroid in asteroids:
        seen = len(can_see(asteroid, asteroids))

        if seen > max_seen:
            max_seen = seen
            base = asteroid

    shot = 0
    shot_angle = -1

    while shot < 200:
        targets = []

        for asteroid in can_see(base, asteroids):
            dx = asteroid[0] - base[0]
            dy = asteroid[1] - base[1]
            angle = 180 - math.degrees(math.atan2(dx, dy))

            if angle <= shot_angle:
                continue

            distance = dx * dx + dy * dy
            targets.append((angle, distance, asteroid))

        if len(targets) == 0:
            shot_angle -= 360
            continue

        targets.sort()
        target = targets[0]
        shot += 1
        asteroids.remove(target[2])
        shot_angle = target[0]

    return target[2][0] * 100 + target[2][1]

def main():
    data = read_input()
    print(part1(data))
    print(part2(data))

if __name__ == "__main__":
    main()
