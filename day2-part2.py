import itertools

checksum = 0

for row in file("day2-input.txt"):
    values = [int(x) for x in row.split("\t")]

    for (a,b) in itertools.permutations(values, 2):
        if a % b == 0:
            checksum += a / b
            break

print checksum