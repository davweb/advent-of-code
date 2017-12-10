input_list = [int(i) for i in file("day10-input.txt").read().split(',')]

position = 0
skip = 0
hash_size = 256
hash = range(hash_size)


for length in input_list:
    for i in range(length / 2):
        a = (position + i) % hash_size
        b = (position + length - i - 1)  % hash_size
        hash[a], hash[b] = hash[b], hash[a]

    position = (position + length + skip) % hash_size
    skip += 1

print hash[0] * hash[1]
