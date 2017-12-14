import operator

HASH_SIZE = 256
SLICE_SIZE = 16

def knot_hash(input):
    input_list = [ord(i) for i in input]
    input_list += [17, 31, 73, 47, 23]
    input_list *= 64

    position = 0
    skip = 0
    hash = range(HASH_SIZE)

    for length in input_list:
        for i in range(length / 2):
            a = (position + i) % HASH_SIZE
            b = (position + length - i - 1)  % HASH_SIZE
            hash[a], hash[b] = hash[b], hash[a]

        position = (position + length + skip) % HASH_SIZE
        skip += 1

    hash = [reduce(operator.xor, hash[i:i + SLICE_SIZE]) for i in range(0, HASH_SIZE, SLICE_SIZE)]
    return hash