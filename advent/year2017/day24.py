from enum import Enum

def read_input():
    file = open('input/2017/day24-input.txt', 'r')
    data = []

    for line in file:
        values = line.strip().split('/')
        data.append((int(values[0]), int(values[1])))    
 
    return data


def weight(chain):
    """
    >>> weight([(1, 1), (2, 2), (3, 3)])
    12
    """

    return sum(sum(link) for link in chain)


def find_chain(beginning, options, better_chain):

    if len(options) == 0:
        return None

    best_chain = None

    for option in options:
        start, end = option

        if beginning is None or start == beginning or end == beginning:
            remaining = list(options)
            remaining.remove(option)
            child = find_chain(end if start == beginning else start, remaining, better_chain)

            new_chain = [option]

            if child is not None:
                new_chain += child

            if best_chain is None or better_chain(best_chain, new_chain):
                best_chain = new_chain

    return best_chain


def longest(beginning, options):
    if len(options) == 0:
        return None

    best_chain = None

    for option in options:
        start, end = option

        if beginning is None or start == beginning or end == beginning:
            remaining = list(options)
            remaining.remove(option)
            child = longest(end if start == beginning else start, remaining)

            new_chain = [option]

            if child is not None:
                new_chain += child

            if best_chain is None or len(new_chain) > len(best_chain) or (len(new_chain) == len(best_chain) and weight(new_chain) > weight(best_chain)):
                best_chain = new_chain

    return best_chain


def part1(data):
    """
    >>> part1(read_input())
    1868
    """

    def strongest(old_chain, new_chain):
        return weight(new_chain) > weight(old_chain)

    chain = find_chain(0, data, strongest)
    return weight(chain)


def part2(data):
    """
    >>> part2(read_input())
    1841
    """

    def longest(old_chain, new_chain):
        old = len(old_chain)
        new = len(new_chain)
        return new > old or (new == old and weight(new_chain) > weight(old_chain))

    chain = find_chain(0, data, longest)
    return weight(chain)


def main():
    data = read_input();
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
