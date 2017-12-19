def read_file(filename):
    network = []

    for line in file(filename):
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

def part1(filename):
    network = read_file(filename)
    steps, visited = visit(network)
    return "".join(visited)

def part2(filename):
    network = read_file(filename)
    steps, visited = visit(network)
    return steps

def main():
    print part1("day19-sample.txt")
    print part1("day19-input.txt")
    print part2("day19-sample.txt")
    print part2("day19-input.txt")

if __name__ == "__main__":
    main()
