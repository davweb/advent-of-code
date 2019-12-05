#!/usr/local/bin/python3

import itertools 
from intcode import IntCode

def read_input():
    return [int(code) for code in open('input/day2-input.txt', 'r').read().split(',')]

def execute(data, noun, verb):
    input = data.copy();
    input[1] = noun
    input[2] = verb
    i = IntCode(input, [])
    i.execute()
    return i.memory[0]

def part1(data):
    print(execute(data, 12 , 2))

def part2(data):
    nouns = range(0, 100)
    verbs = range(0, 100)

    for (noun, verb) in itertools.product(nouns, verbs):
        if execute(data, noun, verb) == 19690720:
            print(100 * noun + verb)
            return

    raise Exception("No result found")


def main():
    data = read_input()
    part1(data)
    part2(data)

if __name__ == "__main__":
    main()
