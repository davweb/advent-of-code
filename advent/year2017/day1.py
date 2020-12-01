#!/usr/local/bin/python3

def read_input():
    file = open('input/2017/day1-input.txt', 'r')
    return file.read()

def part1(captcha):
    """
    >>> part1("91212129")
    9
    >>> part1(read_input())
    1029
    """
   
    prev = captcha[0]
    captcha += prev
    total = 0

    for c in captcha[1:]:
        curr = int(c)
        if curr == prev:
            total += curr
        prev = curr

    return total


def part2(captcha):
    """
    >>> part2("1212")
    6
    >>> part2("12131415")
    4
    >>> part2(read_input())
    1220
    """
    
    half = len(captcha) // 2
    rotated = captcha[half:] + captcha[:half] 
    total = 0

    for (a,b) in zip(captcha, rotated):
        if a == b:
            total += int(a)

    return total

def main():
    data = read_input()
    print(part1(data))
    print(part2(data))

if __name__ == "__main__":
    main()
