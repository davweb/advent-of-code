banks = [int(bank) for bank in file('day6-input.txt').read().split()]

prev = set()
count = 0

def fullest_bank():
    i = 0
    max = -1

    while i < len(banks):
        if banks[i] > max:
            max_index = i
            max = banks[i]
        i += 1

    return max_index

while tuple(banks) not in prev:
    prev.add(tuple(banks))
    count += 1

    i = fullest_bank()
    redist = banks[i]
    banks[i] = 0

    while redist > 0:
        i = i + 1
        if i == len(banks):
            i = 0
        banks[i] += 1
        redist -= 1

print count