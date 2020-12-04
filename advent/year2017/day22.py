from enum import Enum

class State(Enum):
    CLEAN = 1
    WEAKENED = 2
    INFECTED = 3
    FLAGGED = 4


class Direction(Enum):
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)


def read_input():
    file = open('input/2017/day22-input.txt', 'r')
    data = []

    for line in file:
        data.append([State.INFECTED if c == '#' else State.CLEAN for c in line.strip()])    
 
    return data


def next_direction(direction, state):
    if state == State.FLAGGED:
        if direction == Direction.UP:
            return Direction.DOWN
        elif direction == Direction.RIGHT:
            return Direction.LEFT
        elif direction == Direction.DOWN:
            return Direction.UP
        else:
            return Direction.RIGHT
    elif state == State.INFECTED:
        if direction == Direction.UP:
            return Direction.RIGHT
        elif direction == Direction.RIGHT:
            return Direction.DOWN
        elif direction == Direction.DOWN:
            return Direction.LEFT
        else:
            return Direction.UP
    elif state == State.CLEAN:
        if direction == Direction.UP:
            return Direction.LEFT
        elif direction == Direction.LEFT:
            return Direction.DOWN
        elif direction == Direction.DOWN:
            return Direction.RIGHT
        else:
            return Direction.UP
    elif state == State.WEAKENED:
        return direction

    raise ValueError("Invalid State '{}'".format(state))


def process(data, state_processor, bursts):
    grid = {}

    for y, row in enumerate(data):
        for x, value in enumerate(row):
            grid[(x,y)] = value
  
    y = len(data) // 2
    x = len(data[0]) // 2
    direction = Direction.UP
    burst = 0
    count = 0

    while burst < bursts:
        burst += 1
        state = grid.get((x,y), State.CLEAN)
        new_state = state_processor(state)
        grid[(x,y)] = new_state

        if new_state == State.INFECTED:
            count += 1

        direction = next_direction(direction, state)
        dx, dy = direction.value
        x += dx
        y += dy

    return count


def part1(data):
    """
    >>> part1(read_input())
    5182
    """

    def next_state(state):
        if state == State.INFECTED:
            return State.CLEAN
        else:
            return State.INFECTED
    
    return process(data, next_state, 10000)


def part2(data):
    """
    >>> part2(read_input())
    2512008
    """
    
    def next_state(state):
        if state == State.INFECTED:
            return State.FLAGGED
        elif state == State.FLAGGED:
            return State.CLEAN
        elif state == State.CLEAN:
            return State.WEAKENED
        elif state == State.WEAKENED:
            return State.INFECTED
        
        raise ValueError("Invalid State '{}'".format(state))

    return process(data, next_state, 10000000)


def main():
    data = read_input();
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
