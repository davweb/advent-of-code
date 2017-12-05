input = 347991

x = 0
y = 0
i = 1
max_x = 0
max_y = 0
min_x = 0
min_y = 0

direction = 'right'

while i < input:
    i += 1

    if direction == 'right':
        x += 1
        if x > max_x:
            max_x = x
            direction = 'up'
    elif direction == 'up':
        y += 1
        if y > max_y:
            max_y = y
            direction = 'left'
    elif direction == 'left':
        x -= 1
        if x < min_x:
            min_x = x
            direction = 'down'
    elif direction == 'down':
        y -= 1
        if y < min_y:
            min_y = y
            direction = 'right'

print "%d (%d,%d) = %d" % (i, x, y, abs(x) + abs(y))