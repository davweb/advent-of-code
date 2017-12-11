input_list = file("day11-input.txt").read().split(',')

DIRECTIONS = {
    'n': (0,2),
    'ne': (1,1),
    'se': (1,-1),
    's': (0,-2),
    'sw': (-1,-1),
    'nw': (-1,1)
}

def distance_home(x,y):
    x,y = abs(x),abs(y)
    steps = 0

    while x != 0 or y != 0:
        if y > x:
            y -= 2
            steps += 1
        elif y < x:
            x -= 2
            steps += 2
        else:
            x -= 1
            y -= 1
            steps += 1

    return steps

x,y = 0,0
furthest = 0

for move in input_list:
    dx,dy = DIRECTIONS[move]
    x += dx
    y += dy
    furthest = max(furthest, distance_home(x,y))

print distance_home(x,y), furthest
