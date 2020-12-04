from enum import Enum

def read_input():
    file = open('input/2017/day23-input.txt', 'r')
    data = []

    for line in file:
        data.append(line.strip().split())    
 
    return data


def part1(data):
    """
    >>> part1(read_input())
    5929
    """

    registers = { 'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 'h': 0 }
    count = 0
    index = 0

    while index >=0 and index < len(data):
        (ins, x, y) = data[index]

        if y.isalpha():
            y = registers[y]
        else:
            y = int(y)

        if ins == 'set':
            registers[x] = y
        elif ins == 'sub':
            registers[x] -= y
        elif ins == 'mul':
            registers[x] *= y
            count += 1
        elif ins == 'jnz':
            if x.isalpha():
                x = registers[x]
            else:
                x = int(x)

            if x != 0:
                index += y
                continue

        index += 1

    return count

def part2():
    """
    >>> part1(read_input())
    907
    """

    b = 107900
    c = b + 17000
    h = 1

    while b < c:
        d = 2
        limit = b // 2

        while d <= limit:
            if b % d == 0:
                h += 1
                break

            d += 1

        b += 17
    
    return h


def main():
    data = read_input();
    print(part1(data))
    print(part2())


if __name__ == "__main__":
    main()
