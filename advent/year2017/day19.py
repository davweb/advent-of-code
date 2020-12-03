def read_input():
    return read_file('input/2017/day19-input.txt')


def read_file(filename):
    network = []

    for line in open(filename, 'r'): #.readlines():
        network.append(line)

    return network


def find_start(network):
    y = 0
    x = 0

    while network[y][x] != '|':
        x += 1

    return (x,y)


def move(direction, x, y):
    if direction == 'N':
        y -= 1
    elif direction == 'S':
        y += 1
    elif direction == 'E':
        x += 1
    elif direction == 'W':
        x -= 1

    return x ,y


def valid_move(network, x, y):
    height = len(network)
    width = len(network[0])
    return x >= 0 and x < width and y >= 0 and y < height and network[y][x] != ' '


def visit(network):
    """
    >>> sample = read_file('input/2017/day19-sample.txt')
    >>> visit(sample)
    (38, ['A', 'B', 'C', 'D', 'E', 'F'])
    """

    x, y = find_start(network)

    direction = 'S'
    visited = []
    steps = 0

    while valid_move(network, x, y):
        steps += 1
        x, y = move(direction, x, y)
        square = network[y][x]

        if square == '+':
            if direction in ['E', 'W']:
                new_directions = ['N', 'S']
            else:
                new_directions = ['E', 'W']

            for new_direction in new_directions:
                newx, newy = move(new_direction, x, y)
                if valid_move(network, newx, newy):
                    direction = new_direction
        elif square not in ['-', '|', ' ']:
            visited.append(square)

    return steps, visited


def part1and2(network):
    """"
    >>> part1and2(read_input())
    ('AYRPVMEGQ', 16408)
    """

    steps, visited = visit(network)
    return ("".join(visited), steps)


def main():
    data = read_input()
    print(part1and2(data))


if __name__ == "__main__":
    main()
