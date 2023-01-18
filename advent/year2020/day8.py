def read_input():
    data = []

    with open('input/2020/day8-input.txt', encoding='utf-8') as file:
        for line in file:
            ins, val = line.split()
            data.append((ins, int(val)))

    return data


def run(data):
    index = 0
    visited = set()
    acc = 0

    while index < len(data) and index not in visited:
        visited.add(index)
        ins, val = data[index]

        if ins == 'nop':
            index += 1
        elif ins == 'acc':
            acc += val
            index += 1
        elif ins == 'jmp':
            index += val
        else:
            raise ValueError(f"Invalid instruction '{ins}'")

    return (acc, index < len(data))


def part1(data):
    """
    >>> part1(read_input())
    1337
    """

    return run(data)[0]


def part2(data):
    """
    >>> part2(read_input())
    1358
    """

    for index in range(0, len(data)):
        copy = list(data)
        ins, val = copy[index]

        if ins == 'nop':
            copy[index] = ('jmp', val)
        elif ins == 'acc':
            continue
        elif ins == 'jmp':
            copy[index] = ('nop', val)
        else:
            raise ValueError(f"Invalid instruction '{ins}'")

        (acc, looped) = run(copy)

        if not looped:
            return acc

    raise ValueError("Result not found")


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
