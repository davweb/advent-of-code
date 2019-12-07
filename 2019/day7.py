#!/usr/local/bin/python3

from intcode import IntCode
import itertools

def read_input():
    return [int(code) for code in open('input/day7-input.txt', 'r').read().split(',')]

def calc_signal(code, phases):
    """
    >>> calc_signal([3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0], [4,3,2,1,0])
    43210
    >>> calc_signal([3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0], [0, 1, 2, 3, 4])
    54321
    """
    signal = 0

    for phase in phases:
        signal = IntCode(code).execute([phase, signal])

    return signal

def max_signal(code):
    """
    >>> max_signal([3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0])
    43210
    >>> max_signal([3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0])
    54321
    >>> max_signal([3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0])
    65210
    """

    return max(calc_signal(code, phases) for phases in itertools.permutations(range(0, 5)))

def calc_feedback(code, phases):
    """
    >>> calc_feedback([3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5], [9,8,7,6,5])
    139629729
    >>> calc_feedback([3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10], [9,7,8,5,6])
    18216
    """
    thrusters = [IntCode(code, [phase]) for phase in phases]
    signal = 0

    for thruster in itertools.cycle(thrusters):
        output = thruster.execute([signal])

        if output is None:
            return signal

        signal = output

def max_feedback(code):
    """
    >>> max_feedback([3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5])
    139629729
    >>> max_feedback([3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10])
    18216
    """

    return max(calc_feedback(code, phases) for phases in itertools.permutations(range(5, 10)))

def part1(code):
    print(max_signal(code))

def part2(code):
    print(max_feedback(code))


def main():
    code = read_input()
    part1(code)
    part2(code)

if __name__ == "__main__":
    main()
