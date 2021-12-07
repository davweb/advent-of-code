# -*- coding: utf-8 -*-

import re


PATTERN = re.compile(r"(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.")
DURATION = 2503


def read_input():
    results = []

    with open('input/2015/day14-input.txt') as file:
        for line in file.readlines():
            match = PATTERN.match(line)
            name, speed, fly, rest = match.group(1, 2, 3, 4)
            results.append((name, int(speed), int(fly), int(rest)))

    return results


class Reindeer:
    def __init__(self, name, speed, fly, rest):
        self.name = name
        self.speed = speed
        self.fly = fly
        self.rest = rest
        self.flying = True
        self.distance = 0
        self.time = 0
        self.next_swap = fly
        self.score = 0

    def point(self):
        self.score += 1

    def move(self):
        if self.flying:
            self.distance += self.speed

        self.time += 1

        if self.time == self.next_swap:
            self.flying = not self.flying
            self.next_swap += self.fly if self.flying else self.rest


def distance(duration, speed, fly, rest):
    """
    >>> distance(1000, 14, 10, 127)
    1120
    >>> distance(1000, 16, 11, 162)
    1056
    >>> distance(10, 1, 20, 7)
    10
    """

    time = 0
    distance = 0
    flying = True

    while time < duration:
        if flying:
            flight_time = min(fly, duration - time)
            distance += speed * flight_time
            time += fly
        else:
            time += rest

        flying = not flying

    return distance


def part1(data):
    """
    >>> part1(read_input())
    2655
    """

    return max(distance(DURATION, speed, fly, rest) for _, speed, fly, rest in data)


def part2(data):
    """
    >>> part2(read_input())
    1059
    """

    reindeers = [Reindeer(*deer) for deer in data]

    for _ in range(DURATION):
        for deer in reindeers:
            deer.move()

        max(reindeers, key=lambda d: d.distance).point()

    return max(deer.score for deer in reindeers)


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
