import advent


def create_map(input):
    map = []

    for row in range(0,128):
        seed = "%s-%d" % (input, row)
        hash = advent.knot_hash(seed)
        hash = "".join("{0:08b}".format(value) for value in hash)
        hash = [int(c) for c in hash]
        map.append(hash)

    return map

def find_first(map):
    for y in range(0,128):
        for x in range(0,128):
            if map[y][x] == 1:
                return (x,y)

    return None
 
def zero(map, x,y):
    if map[y][x] == 0:
        return
    
    map[y][x] = 0
    if x > 0:
        zero(map, x - 1, y)
    if y > 0:
        zero(map, x, y - 1)
    if x < 127:
        zero(map, x + 1, y)
    if y < 127:
        zero(map, x, y + 1)    


map = create_map("jxqlasbh")
print sum(sum(row) for row in map)

c = find_first(map)
count = 0

while c is not None:
    count += 1
    x,y = c
    zero(map, x, y)
    c = find_first(map)

print count