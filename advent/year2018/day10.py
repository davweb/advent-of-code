#!/usr/local/bin/python3

import re
from advent import bounds

PATTERN = re.compile(r"position=<([- ]\d+), ([- ]\d+)> velocity=<([- ]\d+), ([- ]\d+)>")


class Light:

    def __init__(self, definition):
        """
        >>> Light("position=<-10478,  42641> velocity=< 1, -4>")
        Light(x=-10478, y=42641, dx=1, dy=-4)
        >>> Light("a")
        Traceback (most recent call last):
        ...
        ValueError: Invalid definition 'a'
        """

        match = PATTERN.match(definition)
        if not match:
            raise ValueError(f"Invalid definition '{definition}'")
        self.x = int(match.group(1))
        self.y = int(match.group(2))
        self.dx = int(match.group(3))
        self.dy = int(match.group(4))

    def point(self):
        """
        >>> light =  Light("position=< 3, -7> velocity=< 0,  0>")
        >>> light.point()
        (3, -7)
        """
        return (self.x, self.y)

    def move(self):
        """
        >>> light =  Light("position=< 5,  11> velocity=< 3, -7>")
        >>> light.move()
        >>> light.point()
        (8, 4)
        """
        self.x += self.dx
        self.y += self.dy

    def back(self):
        """
        >>> light =  Light("position=< 5,  11> velocity=< 3, -7>")
        >>> light.back()
        >>> light.point()
        (2, 18)
        """
        self.x -= self.dx
        self.y -= self.dy

    def __repr__(self):
        return "Light(x={x}, y={y}, dx={dx}, dy={dy})".format(**self.__dict__)


def read_input():
    with open('input/2018/day10-input.txt', encoding='utf-8') as file:
        return [Light(line) for line in file]


def area(points):
    """
    >>> area([(0,0), (7, 8)])
    56
    """
    (left, top), (right, bottom) = bounds(points)
    width = abs(right - left)
    height = abs(top - bottom)
    return width * height


def output(lights):
    (left, top), (right, bottom) = bounds([light.point() for light in lights])
    output_value = []

    for y in range(top, bottom + 1):
        line = []

        for x in range(left, right + 1):
            if next((True for light in lights if light.point() == (x, y)), False):
                line.append("█")
            else:
                line.append(" ")

        output_value.append("".join(line))

    return "\n".join(output_value)


def part1and2(lights):
    """
    >>> from advent import md5
    >>> output = part1and2(read_input())
    >>> md5(output[0])
    'a72b6658dc84b74b1f1ecdfa0a2f98b9'
    >>> output[1]
    10612
    """

    size = area([light.point() for light in lights])
    last_size = size
    seconds = 0

    # Keep moving lights until they start to spread apart again
    while size <= last_size:
        last_size = size
        seconds += 1

        for light in lights:
            light.move()

        size = area([light.point() for light in lights])

    # move back to smallest state
    for light in lights:
        light.back()
    seconds -= 1

    return (output(lights), seconds)


def main():
    lights = read_input()
    result = part1and2(lights)
    print(f"{result[0]}\n{result[1]}")


if __name__ == "__main__":
    main()
