# -*- coding: utf-8 -*-

INPUT = ((85, 145), (-163, -108))


def my_function(input_arg):
    """
    >>> my_function(12)
    12
    >>> my_function(14)
    14
    """

    return input_arg


def trajectory(target_x, target_y, x_velocity, y_velocity):
    """
    >>> trajectory((20, 30), (10, -5), 7, 2)
    (True, 3)
    >>> trajectory((20, 30), (10, -5), 6, 3)
    (True, 6)
    >>> trajectory((20, 30), (10, -5), 9, 0)
    (True, 0)
    >>> trajectory((20, 30), (10, -5), 14, -4)
    (False, -4)
    """

    target_min_x, target_max_x = target_x
    target_min_y, target_max_y = target_y

    if target_max_x < target_min_x:
        target_min_x, target_max_x = target_max_x, target_min_x

    if target_max_y < target_min_y:
        target_min_y, target_max_y = target_max_y, target_min_y

    x, y = (0, 0)
    hit_target = False
    height = None

    while x < target_max_x and y > target_min_y:
        x += x_velocity
        y += y_velocity

        if height is None:
            height = y
        else:
            height = max(y, height)

        if x_velocity > 0:
            x_velocity -= 1
        elif x_velocity < 0:
            x_velocity += 1

        y_velocity -= 1

        if target_min_x <= x <= target_max_x and target_min_y <= y <= target_max_y:
            hit_target = True
            break

    return (hit_target, height)


def part1(data):
    """
    >>> part1(((20, 30), (-10, -5)))
    45
    >>> part1(INPUT)
    13203
    """

    target_x, target_y = data
    best = None

    for dx in range(1, max(target_x) + 1):
        for dy in range(0, - min(target_y) + 1):
            hit_target, height = trajectory(target_x, target_y, dx, dy)

            if hit_target:
                if best is None:
                    best = height
                else:
                    best = max(best, height)

    return best


def part2(data):
    """
    >>> part2(((20, 30), (-10, -5)))
    112
    >>> part2(INPUT)
    5644
    """

    target_x, target_y = data
    count = 0
    target_min_y = min(target_y)

    for dx in range(1, max(target_x) + 1):
        for dy in range(target_min_y, - target_min_y + 1):
            hit_target, _ = trajectory(target_x, target_y, dx, dy)

            if hit_target:
                count += 1

    return count


def main():
    print(part1(INPUT))
    print(part2(INPUT))


if __name__ == "__main__":
    main()
