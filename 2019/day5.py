#!/usr/local/bin/python3

from intcode import IntCode

def read_input():
    return [int(code) for code in open('input/day5-input.txt', 'r').read().split(',')]


        

def part1(data):
    i = IntCode(data, [1])

    while True:
        output = i.execute()
        if output is None:
            break
        result = output

    print(result)

    

def part2(data):
    print(IntCode(data).execute([5]))


def main():
    data = read_input()
    part1(data)
    part2(data)

if __name__ == "__main__":
    main()
