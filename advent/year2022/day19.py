# -*- coding: utf-8 -*-
# pylint: disable=line-too-long,too-many-arguments,too-many-locals

from heapq import heappush, heappop
import re

PATTERN = re.compile(r'Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.')


def read_input():
    output = []

    with open('input/2022/day19-input.txt', encoding='utf8') as file:
        for line in file:
            match = PATTERN.match(line)
            output.append([int(i) for i in match.groups()])

    return output


def invert(t):
    a, b, c, d = t
    return (-a, -b, -c, -d)


def upper_bound(geos, geo_robots, minute, time_limit):
    while minute < time_limit:
        geos += geo_robots
        geo_robots += 1
        minute += 1

    return geos


class Calvacade:
    def __init__(self):
        self.seen = {}
        self.queue = []

    def has_next(self):
        return bool(self.queue)

    def pop(self):
        _, robots, totals, minutes = heappop(self.queue)
        return (robots, totals, minutes)

    def push(self, robots, totals, minutes):
        key = (robots, totals)

        if self.seen.get(key, 99) < minutes:
            return

        self.seen[key] = minutes
        priority = (invert(robots), invert(totals))
        heappush(self.queue, (priority, robots, totals, minutes))


def process(
        ore_ore_cost,
        clay_ore_cost,
        obsidian_ore_cost,
        obsidian_clay_cost,
        geode_ore_cost,
        geode_obsidian_cost,
        time_limit=24):
    """
    >>> process(4, 2, 3, 14, 2, 7)
    9
    >>> process(2, 3, 3, 8, 3, 12)
    12
    """

    costs = [
        [0, geode_obsidian_cost, 0, geode_ore_cost, 0],
        [0, 0, obsidian_clay_cost, obsidian_ore_cost],
        [0, 0, 0, clay_ore_cost],
        [0, 0, 0, ore_ore_cost]
    ]

    queue = Calvacade()

    queue.push((0, 0, 0, 1), (0, 0, 0, 0), 0)
    best = 0

    while queue.has_next():
        robots, totals, minute = queue.pop()

        if upper_bound(totals[0], robots[0], minute, time_limit) <= best:
            continue

        if minute == time_limit:
            best = max(best, totals[0])
            continue

        # updated_totals = tuple(total + collected for total, collected in zip(totals, robots))
        # unrolled to
        updated_totals = (totals[0] + robots[0], totals[1] + robots[1], totals[2] + robots[2], totals[3] + robots[3])
        queue.push(robots, updated_totals, minute + 1)

        for robot_index, robot_cost in enumerate(costs):
            # if all(cost <= total for cost, total in zip(robot_cost, totals)):
            # unrolled to:
            if robot_cost[0] <= totals[0] and robot_cost[1] <= totals[1] and robot_cost[2] <= totals[2] and robot_cost[3] <= totals[3]:
                # new_totals = tuple(total - cost for total, cost in zip(updated_totals, robot_cost))
                # unrolled to
                new_totals = (
                    updated_totals[0] - robot_cost[0],
                    updated_totals[1] - robot_cost[1],
                    updated_totals[2] - robot_cost[2],
                    updated_totals[3] - robot_cost[3])

                new_robots = list(robots)
                new_robots[robot_index] += 1
                new_robots = tuple(new_robots)

                queue.push(new_robots, new_totals, minute + 1)

    return best


def part1(data):
    """
    # Too slow to run
    # >>> part1(data)
    # 1092
    """

    quality = 0

    for blueprint, ore_ore_cost, clay_ore_cost, obsidian_ore_cost, obsidian_clay_cost, geode_ore_cost, geode_obsidian_cost in data:
        best = process(
            ore_ore_cost,
            clay_ore_cost,
            obsidian_ore_cost,
            obsidian_clay_cost,
            geode_ore_cost,
            geode_obsidian_cost)
        quality += blueprint * best

    return quality


def part2(data):
    """
    # Too slow to run
    # >>> part2(read_input())
    # 3542
    """

    total = 0

    for _, ore_ore_cost, clay_ore_cost, obsidian_ore_cost, obsidian_clay_cost, geode_ore_cost, geode_obsidian_cost in data[
            0:3]:
        total += process(ore_ore_cost, clay_ore_cost, obsidian_ore_cost,
                         obsidian_clay_cost, geode_ore_cost, geode_obsidian_cost, 32)

    return total


def main():
    print(part1(read_input()))
    print(part2(read_input()))


if __name__ == "__main__":
    main()
