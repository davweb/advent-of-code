#!/usr/local/bin/python3

import itertools 

def read_input():
    return [int(code) for code in open('input/day2-input.txt', 'r').read().split(',')]

def intcode(input):
    """An Intcode program is a list of integers separated by commas (like
    1,0,0,3,99). To run one, start by looking at the first integer (called
    position 0). Here, you will find an opcode - either 1, 2, or 99. The
    opcode indicates what to do; for example, 99 means that the program is
    finished and should immediately halt. Encountering an unknown opcode means
    something went wrong.

    Opcode 1 adds together numbers read from two positions and stores the
    result in a third position. The three integers immediately after the
    opcode tell you these three positions - the first two indicate the
    positions from which you should read the input values, and the third
    indicates the position at which the output should be stored.

    For example, if your Intcode computer encounters 1,10,20,30, it should
    read the values at positions 10 and 20, add those values, and then
    overwrite the value at position 30 with their sum.

    Opcode 2 works exactly like opcode 1, except it multiplies the two inputs
    instead of adding them. Again, the three integers after the opcode
    indicate where the inputs and outputs are, not their values.
 
    Once you're done processing an opcode, move to the next one by stepping
    forward 4 positions.

    >>> intcode([1,0,0,0,99])
    [2, 0, 0, 0, 99]
    >>> intcode([2,3,0,3,99])
    [2, 3, 0, 6, 99]
    >>> intcode([2,4,4,5,99,0])
    [2, 4, 4, 5, 99, 9801]
    >>> intcode([1,1,1,4,99,5,6,0,99])
    [30, 1, 1, 4, 2, 5, 6, 0, 99]
    """

    output = input.copy()
    index = 0

    while True:
        op_code = output[index]

        if op_code == 1 or op_code == 2:
            left_index = output[index + 1]
            right_index = output[index + 2]
            destination_index = output[index + 3]
            left = output[left_index]
            right = output[right_index]

            if op_code == 1:
                result = left + right
            else:
                result = left * right

            output[destination_index] = result

        elif op_code == 99:
            return output

        else:
            raise Exception("Invalid op code {}".format(op_code))

        index += 4

def execute(data, noun, verb):
    input = data.copy();
    input[1] = noun
    input[2] = verb
    return intcode(input)[0]

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
