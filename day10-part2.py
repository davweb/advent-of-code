import advent

hash = advent.knot_hash(file("day10-input.txt").read())
hash = "".join(hex(i)[2:] for i in hash)

print hash
