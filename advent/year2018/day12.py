#!/usr/local/bin/python3

import re
from collections import defaultdict
from itertools import count

STATE_PATTERN = re.compile(r"^initial state: ([#|.]{100})$")
NOTE_PATTERN = re.compile(r"^([#|.]{5}) => ([#|.])$")

class Note:

    def __init__(self, definition):
        """
        >>> Note("###.# => #")
        Note(pattern=[True, True, True, False, True], grows=True)
        >>> Note("a")
        Traceback (most recent call last):
        ...
        ValueError: Invalid defintion 'a'
        """

        match = NOTE_PATTERN.match(definition)
        if not match:
            raise ValueError("Invalid defintion '{}'".format(definition))
        self.pattern = [pot == "#" for pot in match.group(1)]
        self.grows = match.group(2) == "#"
    
    def match(self, pots):
        return self.pattern == pots

    def __repr__(self):
        return "Note(pattern={pattern}, grows={grows})".format(**self.__dict__)

def read_input():
    with open('input/2018/day12-input.txt', 'r') as file:
        match = STATE_PATTERN.match(file.readline())

        state = defaultdict(bool)
        for (index, pot) in zip(count(), match.group(1)):
            if pot == "#":
                state[index] = True
        
        file.readline()
        notes = [Note(line) for line in file.readlines()]
        return(state, notes)

def next_generation(state, notes):
    next_state = defaultdict(bool)
    start = min(state.keys()) - 2 
    end = max(state.keys()) + 3

    for i in range(start, end):
        pots = [state[j] for j in range(i - 2, i + 3)]

        for note in notes:
            if note.match(pots):
                if note.grows:
                    next_state[i] = True
                break

    return next_state


def part1(state, notes):
    """
    >>> part1(*read_input())
    3337
    """

    generation = 0

    while generation < 20:
        generation += 1
        state = next_generation(state, notes)
        
    return sum(state.keys())


def part2(state, notes):
    """
    >>> part2(*read_input())
    4300000000349
    """

    previous_pots = None
    previous_score = None
    generation = 0
    
    while True:
        generation += 1
        
        next_state = next_generation(state, notes)

        # Have to calculate score here as creating pots string will distort the score
        score = sum(next_state.keys())

        start = min(next_state.keys())
        end = max(next_state.keys()) + 1
        pots = ''

        for i in range(start, end):
            pots += "#" if next_state[i] else '.'

        if pots == previous_pots:
            step = score - previous_score
            offset = score - generation * step
            return 50000000000 * step + offset

        previous_pots = pots
        previous_score = score
        state = next_state


def main():
    (state, notes) = read_input()
    print(part1(state, notes))
    print(part2(state, notes))


if __name__ == "__main__":
    main()
