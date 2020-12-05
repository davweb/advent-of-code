def read_input():
    file = open('input/2020/day5-input.txt', 'r')
    return [line.strip() for line in file]


def split(range, upper):
    """
    >>> split((0, 127), False)
    (0, 63)
    >>> split((0, 63), True)
    (32, 63)
    >>> split((32, 63), False)
    (32, 47)
    >>> split((32, 47), True)
    (40, 47)
    >>> split((40, 47), True)
    (44, 47)
    >>> split((44, 47), False)
    (44, 45)
    >>> split((44, 45), False)
    (44, 44)
    >>> split((0, 7), True)
    (4, 7)
    >>> split((4, 7), False)
    (4, 5)
    >>> split((4, 5), True)
    (5, 5)
    """

    start, end = range
    length = (end - start + 1) // 2
    
    if upper:
        return (start + length, end)
    else:
        return (start, end - length)


def seat_id(directions):
    """
    >>> seat_id("BFFFBBFRRR")
    567
    >>> seat_id("FFFBBBFRRR")
    119
    >>> seat_id("BBFFBBFRLL")
    820
    """

    row = (0, 127)
    seat = (0, 7)

    for c in directions[0:7]:
        row = split(row, c == 'B')

    for c in directions[7:]:
        seat = split(seat, c == 'R')

    return row[0] * 8 + seat[0]


def part1(data):
    """
    >>> part1(read_input())
    835
    """
    
    return max(seat_id(directions) for directions in data)


def part2(data):
    """
    >>> part2(read_input())
    649
    """
    
    previous = 0

    for seat in sorted(seat_id(directions) for directions in data): 
        if seat - previous == 2:
            return seat - 1

        previous = seat

    raise ValueError('Seat not found') 


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
