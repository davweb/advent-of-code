input = 347991

x = 0
y = 0
i = 1
value = 1
max_x = 0
max_y = 0
min_x = 0
min_y = 0

direction = 'right'
values = {}
values[(0,0)] = 1

def adjacent(x, y):
    try:
        return values[(x,y)]
    except KeyError:
        return 0


while value < input:
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

    value = adjacent(x - 1, y - 1) + adjacent(x, y - 1) + adjacent(x + 1, y - 1) + adjacent(x - 1, y) + adjacent(x + 1, y) + adjacent(x - 1, y + 1) + adjacent(x, y + 1) + adjacent(x + 1, y + 1)
    
    values[(x,y)] = value

print value
