def part1(step):
    max_value = 2017
    cycle_buffer = [0]
    position = 0

    for value in xrange(1, max_value + 1):
        position = (position + step) % len(cycle_buffer) + 1
        cycle_buffer.insert(position, value)

    position = (position + 1) % len(cycle_buffer)
    return cycle_buffer[position]

def part2(step):
    max_value = 50000000
    buffer_size = 1
    position = 0
    current = None

    for value in xrange(1, max_value + 1):
        position = (position + step) % buffer_size + 1
        buffer_size += 1
        if position == 1:
            current = value
    
    return current

def main():
    print part1(3), part1(303), part2(303)

if __name__ == "__main__":
    main()
