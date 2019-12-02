valid = 0

for line in file('day4-input.txt'):
    words = [''.join(sorted(word)) for word in line.split()]
    unique = set(words)
    if len(words) == len(unique):
        valid += 1

print valid