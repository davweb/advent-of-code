valid = 0

for line in file('day4-input.txt'):
    words = line.split()
    unique = set(words)
    if len(words) == len(unique):
        valid += 1

print valid