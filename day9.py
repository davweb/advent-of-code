score = 0
depth = 0
garbage = False
garbage_count = 0
ignore = False

for char in file('day9-input.txt').read():
    if ignore:
        ignore = False
    elif char == '!':
        ignore = True
    elif garbage:
        if char == '>':
            garbage = False
        else:
            garbage_count += 1
    elif char == '<':
        garbage = True
    elif char == '{':
        depth += 1
    elif char == '}':
        score += depth
        depth -= 1

print score, garbage_count
