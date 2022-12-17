# -*- coding: utf-8 -*-
# pylint: disable=too-many-instance-attributes

import re
from heapq import heappush, heappop

PATTERN = re.compile(r'Valve ([A-Z]{2}) has flow rate=(\d+); tunnels? leads? to valves? ([A-Z]{2}(, [A-Z]{2})*)')


def read_input(filename='input/2022/day16-input.txt'):
    output = []

    with open(filename, encoding='utf8') as file:
        for line in file:
            match = PATTERN.match(line)
            if match is None:
                print(line)
            output.append((match.group(1), int(match.group(2)), match.group(3).split(', ')))

    return output


class Node:

    @classmethod
    def load_valves(cls, data):
        Node._valve_id = {}
        Node._rates = []
        Node._tunnels = []
        Node._valve_count = None

        for index, (valve, _, _) in enumerate(data):
            Node._valve_id[valve] = index

        for valve, valve_rate, valve_tunnels in data:
            Node._rates.append(valve_rate)
            Node._tunnels.append(tuple(Node._valve_id[v] for v in valve_tunnels))

        Node._max_rate = sum(Node._rates)
        Node._valve_count = sum(1 for rate in Node._rates if rate > 0)
        Node._start = Node._valve_id['AA']

    def __init__(self, using_elephants=True, max_time=26):
        self.using_elephants = using_elephants
        self.max_time = max_time

        self.person = Node._start
        self.elephant = Node._start
        self.open_valves = ()
        self.minute = 0
        self.released = 0

        #  These are cache of values that are calculated from the above
        self.rate = 0
        self.open_valve_count = 0
        self.pending = 0
        self.finished = False

    def copy(self):
        copy_node = Node(self.using_elephants, self.max_time)

        copy_node.person = self.person
        copy_node.elephant = self.elephant
        copy_node.open_valves = self.open_valves
        copy_node.minute = self.minute
        copy_node.released = self.released

        copy_node.rate = self.rate
        copy_node.open_valve_count = self.open_valve_count
        copy_node.pending = self.pending
        copy_node.finished = self.finished
        return copy_node

    def lower_bound(self):
        return self.released + self.rate * (self.max_time - self.minute)

    def upper_bound(self):
        return self.released + Node._max_rate * (self.max_time - self.minute)

    def next_nodes(self):
        after = self.copy()
        after.process()

        for person_node in after.next_person():
            if self.using_elephants:
                for elephant_node in person_node.next_elephant():
                    elephant_node.calc_pending()
                    yield elephant_node
            else:
                yield person_node

    def turn_on_valve(self, valve):
        self.open_valves = tuple(sorted(self.open_valves + (valve,)))
        self.open_valve_count += 1
        self.rate += Node._rates[valve]

    def next_elephant(self):
        for next_elephant in Node._tunnels[self.elephant]:

            if next_elephant == self.person:
                continue

            node = self.copy()
            node.elephant = next_elephant
            yield node

        if self.elephant not in self.open_valves and Node._rates[self.elephant] > 0:
            node = self.copy()
            node.turn_on_valve(self.elephant)
            yield node

    def next_person(self):
        for next_person in Node._tunnels[self.person]:
            node = self.copy()
            node.person = next_person
            yield node

        if self.person not in self.open_valves and Node._rates[self.person] > 0:
            node = self.copy()
            node.turn_on_valve(self.person)
            yield node

    def process(self):
        self.minute += 1
        self.released += self.rate
        self.finished = self.minute == self.max_time or self.open_valve_count == Node._valve_count

    def calc_pending(self):
        pending = self.rate
        if self.elephant not in self.open_valves:
            pending += Node._rates[self.elephant]

        if self.person not in self.open_valves:
            pending += Node._rates[self.person]

        self.pending = pending

    def cache_key(self):
        if self.elephant < self.person:
            return (self.elephant, self.person, self.minute, self.open_valves)
        return (self.person, self.elephant, self.minute, self.open_valves)

    def __lt__(self, other):
        if self.open_valve_count != other.open_valve_count:
            return self.open_valve_count > other.open_valve_count

        if self.pending != other.pending:
            return self.pending > other.pending

        if self.rate != other.rate:
            return self.rate > other.rate

        return self.minute < other.minute


def search(start_node):
    """
    >>> data = read_input('input/2022/day16-test.txt')
    >>> Node.load_valves(data)
    >>> node = Node(False, 30)
    >>> search(node)
    1651
    >>> node = Node(True, 26)
    >>> search(node)
    1707
    """

    queue = []
    heappush(queue, start_node)
    best = 0
    seen = {}

    while queue:
        node = heappop(queue)

        if node.upper_bound() <= best:
            continue

        lower_bound = node.lower_bound()
        cache_key = node.cache_key()

        if cache_key in seen:
            if seen[cache_key] >= lower_bound:
                continue

        seen[cache_key] = lower_bound

        if node.finished:
            best = max(best, lower_bound)
            continue

        for next_node in node.next_nodes():
            heappush(queue, next_node)

    return best


def part1(data):
    """
    >>> part1(read_input())
    1638
    """

    Node.load_valves(data)
    return search(Node(False, 30))


def part2(data):
    """
    # Takes too long to run
    # >>> part2(read_input())
    # 2400
    """

    Node.load_valves(data)
    return search(Node(True, 26))


def main():
    print(part1(read_input()))
    print(part2(read_input()))


if __name__ == "__main__":
    main()
