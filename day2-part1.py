checksum = 0

for row in file("day2-input.txt"):
    values = [int(x) for x in row.split("\t")]
    checksum += max(values) - min(values)

print checksum