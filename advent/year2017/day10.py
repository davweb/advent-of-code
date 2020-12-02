from advent import knot_hash, bytes_to_hex

def read_input():
    file = open('input/2017/day10-input.txt', 'r')
    return file.read()

def part1(data):
    """
    >>> part1(read_input())
    20056
    """
    data = [int(i) for i in data.split(',')]

    position = 0
    skip = 0
    hash_size = 256
    hash = list(range(hash_size))


    for length in data:
        for i in range(length // 2):
            a = (position + i) % hash_size
            b = (position + length - i - 1)  % hash_size
            hash[a], hash[b] = hash[b], hash[a]

        position = (position + length + skip) % hash_size
        skip += 1

    return hash[0] * hash[1]


def part2(data):
    """
    >>> part2(read_input())
    'd9a7de4a809c56bf3a9465cb84392c8e'
    """

    hash = knot_hash(data)
    return bytes_to_hex(hash)

def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()