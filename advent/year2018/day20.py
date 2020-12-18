# -*- coding: utf-8 -*-


def read_input():
    file = open("input/2018/day20-input.txt", "r")
    return file.read().strip()


def count_doors(regex):
    """
    >>> count_doors("^WNE$")
    3
    >>> count_doors("^ENWWW(NEEE|SSE(EE|N))$")
    10
    >>> count_doors("^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$")
    18
    >>> count_doors("^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$")
    23
    >>> count_doors("^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$")
    31
    """

    groups = []
    group = [0]

    for i in regex:
        if i in ('N', 'S', 'E', 'W'):
            group[-1] += 1
        elif i == '(':
            groups.append(group)
            group = [0]
        elif i == '|':
            group.append(0)
        elif i == ')':
            length = 0 if min(group) == 0 else max(group)
            group = groups.pop()
            group[-1] += length

    return group[0]


def parse_regex(regex):
    """
    >>> parse_regex("^WNE$")
    ['W', 'N', 'E']
    >>> parse_regex("NEEE|S")
    (['N', 'E', 'E', 'E'], 'S')
    >>> parse_regex("NEEE(S)")
    ['N', 'E', 'E', 'E', 'S']
    >>> parse_regex("^W(NSEW|)E$")
    ['W', (['N', 'S', 'E', 'W'], []), 'E']
    >>> parse_regex("N(WSSNNE|)(N|E)")
    ['N', (['W', 'S', 'S', 'N', 'N', 'E'], []), ('N', 'E')]
    """

    # First check if we have any | and split the regex there and call recursively
    or_indexes = []
    brackets = 0

    for index, c in enumerate(regex):
        # We need to ignore | inside brackets
        if c == '(':
            brackets += 1
        elif c == ')':
            brackets -= 1
        elif c == '|' and brackets == 0:
            or_indexes.append(index)

    if or_indexes:
        start = 0
        options = []

        for end in or_indexes:
            options.append(parse_regex(regex[start:end]))
            start = end + 1

        options.append(parse_regex(regex[start:]))
        return tuple(options)

    group = []
    i = 0

    # Go through the regex, processing expressions in brackets recursively
    while(i < len(regex)):
        c = regex[i]

        if c in ('N', 'S', 'E', 'W'):
            group.append(c)
            i += 1
        elif c == '(':
            brackets = 1
            j = i + 1

            while brackets > 0:
                c = regex[j]
                j += 1

                if c == '(':
                    brackets += 1
                elif c == ')':
                    brackets -= 1

            group.append(parse_regex(regex[i + 1:j - 1]))
            i = j
        else:
            i += 1

    return group[0] if len(group) == 1 else group


def follow_directions(directions, doors = None, x = 0, y = 0):

    if doors is None:
        doors = set()

    for d in directions:

        if type(d) == list:
            (_, x, y) = follow_directions(d, doors, x, y)

        elif type(d) == tuple:
            checkpoint_x, checkpoint_y = x, y

            for option in d:
                (_, x, y) = follow_directions(option, doors, checkpoint_x, checkpoint_y)

        elif d == 'N':
            doors.add((x, y, 'N'))
            y += 1

        elif d == 'S':
            doors.add((x, y - 1, 'N'))
            y -= 1

        elif d == 'E':
            doors.add((x, y, 'E'))
            x += 1

        elif d == 'W':
            doors.add((x - 1, y, 'E'))
            x -= 1

    return (doors, x, y)


def possible_doors(location):
    x, y = location

    return (
        ((x + 1, y), (x, y, 'E')),
        ((x - 1, y), (x - 1, y, 'E')),
        ((x, y + 1), (x, y, 'N')),
        ((x, y - 1), (x, y - 1, 'N'))
    )


def traverse(doors):
    distance_map = {}
    start_location = (0, 0)
    queue = [start_location]
    distance_map[start_location] = 0

    while queue:
        location = queue.pop(0)
        next_distance = distance_map[location] + 1

        for (next_location, door) in possible_doors(location):
            if door in doors and (next_location not in distance_map or distance_map[next_location] > next_distance):
                distance_map[next_location] = next_distance
                queue.append(next_location)

    return distance_map


def part1(data):
    """
    >>> part1(read_input())
    3669
    """

    return count_doors(data)


def part2(data):
    """
    >>> part2(read_input())
    8369
    """

    directions = parse_regex(data)
    (doors, _, _) = follow_directions(directions)
    distance_map = traverse(doors)
    return sum(1 for distance in distance_map.values() if distance >= 1000)


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
