instructions = [int(line) for line in file('day5-input.txt')]

size = len(instructions)
index = 0
count = 0

while 0 <= index < size:
    jump = instructions[index]
    instructions[index] += 1
    index += jump
    count += 1

print count