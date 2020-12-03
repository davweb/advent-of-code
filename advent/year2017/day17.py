INPUT = 303


def spinlock(step):
    """
    >>> spinlock(3)
    638
    """

    max_value = 2017
    cycle_buffer = [0]
    position = 0

    for value in range(1, max_value + 1):
        position = (position + step) % len(cycle_buffer) + 1
        cycle_buffer.insert(position, value)

    position = (position + 1) % len(cycle_buffer)
    return cycle_buffer[position]


def part1():
    """
    >>> part1()
    1971
    """

    return spinlock(INPUT)


def part2():
    """
    >>> part2()
    17202899
    """

    max_value = 50000000
    buffer_size = 1
    position = 0
    current = None
    step = INPUT

    for value in range(1, max_value + 1):
        position = (position + step) % buffer_size + 1
        buffer_size += 1
        if position == 1:
            current = value
    
    return current


def main():
    print(part1())
    print(part2())


if __name__ == "__main__":
    main()
