import operator

input_list = [ord(i) for i in file("day10-input.txt").read()]
input_list += [17, 31, 73, 47, 23]
input_list *= 64

position = 0
skip = 0
hash_size = 256
slice_size = 16
hash = range(hash_size)


for length in input_list:
    for i in range(length / 2):
        a = (position + i) % hash_size
        b = (position + length - i - 1)  % hash_size
        hash[a], hash[b] = hash[b], hash[a]

    position = (position + length + skip) % hash_size
    skip += 1

hash = [reduce(operator.xor, hash[i:i + slice_size]) for i in range(0, hash_size, slice_size)]
hash = "".join(hex(i)[2:] for i in hash)

print hash
