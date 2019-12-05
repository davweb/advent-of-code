#!/usr/local/bin/python3

from functools import total_ordering
from collections import defaultdict
from datetime import datetime
import operator
import re

PATTERN = re.compile(r"\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2})\] (Guard #(\d+) begins shift|wakes up|falls asleep)")

@total_ordering
class Event:

    def __init__(self, definition):
        """
        >>> Event("[1518-04-10 00:04] Guard #2467 begins shift")
        Event(datetime="1518-04-10 00:04:00", type="GUARD", guard_id=2467)
        >>> Event("[1518-05-24 00:56] wakes up")
        Event(datetime="1518-05-24 00:56:00", type="WAKE", guard_id=None)
        >>> Event("[1518-04-15 00:57] falls asleep")
        Event(datetime="1518-04-15 00:57:00", type="SLEEP", guard_id=None)
        >>> Event("a")
        Traceback (most recent call last):
        ...
        ValueError: Invalid defintion 'a'
        """

        match = PATTERN.match(definition)

        if not match:
            raise ValueError("Invalid defintion '{}'".format(definition))

        self.datetime = datetime.strptime(match.group(1), "%Y-%m-%d %H:%M")
        self.guard_id = int(match.group(3)) if match.group(3) else None

        description = match.group(2)

        if description == "wakes up":
            self.type = 'WAKE'
        elif description == "falls asleep":
            self.type = 'SLEEP'
        else:
            self.type = 'GUARD'

    def minutes_until(self, other):
        """
        >>> wake = Event("[1518-05-24 00:00] wakes up")
        >>> sleep = Event("[1518-05-24 00:01] falls asleep")
        >>> sleep_later = Event("[1518-05-24 00:57] falls asleep")
        >>> wake.minutes_until(wake)
        0
        >>> wake.minutes_until(sleep)
        1
        >>> wake.minutes_until(sleep_later)
        57
        """

        delta = other.datetime - self.datetime
        return int(delta.total_seconds() // 60)

    def __lt__(self, other):
        return self.datetime < other.datetime

    def __eq__(self, other):
        # Assuming timestamps are uniques  
        return self.datetime == other.datetime
    
    def __repr__(self):
        return 'Event(datetime="{datetime}", type="{type}", guard_id={guard_id})'.format(**self.__dict__)

def read_input():
    file = open('input/day4-input.txt', 'r')
    return sorted(Event(line) for line in file.readlines())

def key_for_largest_value(some_dict):
    return max(some_dict.items(), key=operator.itemgetter(1))[0]

def sleepiest_guard(events):
    time_asleep = defaultdict(int)

    for event in events:
        if event.type == 'GUARD':
            guard_id = event.guard_id
        elif event.type == 'SLEEP':
            sleep = event
        else:
            wake = event
            time = sleep.minutes_until(wake)
            time_asleep[guard_id] += time

    return key_for_largest_value(time_asleep)

def process_events(events):
    """
    >>> guard = Event("[1518-05-24 00:01] Guard #7 begins shift")
    >>> sleep = Event("[1518-05-24 00:02] falls asleep")
    >>> wake = Event("[1518-05-24 00:12] wakes up")
    >>> events = [guard, sleep, wake]
    >>> result = process_events(events)
    >>> result[7][3]
    1
    >>> result[7][9]
    1
    >>> result[7][20]
    0
    >>> result[1][3]
    0
    """

    # sleeps by guard then by minute
    minutes_sleeping = defaultdict(lambda: defaultdict(int))

    for event in events:
        if event.type == 'GUARD':
            guard_id = event.guard_id
        elif event.type == 'SLEEP':
            sleep = event
        else:
            wake = event
            for minute in range(sleep.datetime.minute, wake.datetime.minute):
                minutes_sleeping[guard_id][minute] += 1

    return minutes_sleeping


def part1(events):
    sleepiest_guard_id = sleepiest_guard(events)
    minutes_sleeping = process_events(events)[sleepiest_guard_id]
    sleepiest_minute = key_for_largest_value(minutes_sleeping)
    print(sleepiest_guard_id * sleepiest_minute)


def part2(events):
    minutes_sleeping = process_events(events)
    sleepiest_guard_id = None
    sleepiest_minute = None
    max_sleeps = 0

    for guard_id in minutes_sleeping:
        for minute in minutes_sleeping[guard_id]:
            sleeps = minutes_sleeping[guard_id][minute]

            if sleeps > max_sleeps:
                max_sleeps = sleeps
                sleepiest_guard_id = guard_id
                sleepiest_minute = minute

    print(sleepiest_guard_id * sleepiest_minute)

def main():
    events = read_input()
    part1(events)
    part2(events)

if __name__ == "__main__":
    main()
