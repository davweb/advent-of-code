# -*- coding: utf-8 -*-

from ast import literal_eval
from itertools import permutations


def read_input():
    with open('input/2021/day18-input.txt', encoding='utf8') as file:
        return [SnailfishNumber(line.strip()) for line in file.readlines()]


class SnailfishNumber:
    """
    >>> SnailfishNumber(1)
    Traceback (most recent call last):
      ...
    ValueError: Not a list: 1
    >>> SnailfishNumber([1])
    Traceback (most recent call last):
      ...
    ValueError: Not a pair: [1]
    """

    def __init__(self, value=None, is_left=None, left=None, right=None):
        if value is not None:
            if isinstance(value, str):
                value = literal_eval(value)

            if not isinstance(value, list):
                raise ValueError(f'Not a list: {value}')

            if len(value) != 2:
                raise ValueError(f'Not a pair: {value}')

            left, right = value

            if isinstance(left, list):
                left = SnailfishNumber(value=left, is_left=True)

            if isinstance(right, list):
                right = SnailfishNumber(value=right, is_left=False)

        self.is_left = is_left
        self.left = left
        self.right = right
        self.parent = None

        if isinstance(left, SnailfishNumber):
            left.parent = self
            left.is_left = True

        if isinstance(right, SnailfishNumber):
            right.parent = self
            right.is_left = False

    def __str__(self):
        """
        >>> str(SnailfishNumber([9,[8,7]]))
        '[9, [8, 7]]'
        """
        return '[{left}, {right}]'.format(**self.__dict__)

    def __repr__(self):
        """
        >>> SnailfishNumber([9, [8, 7]])
        SnailfishNumber([9, [8, 7]])
        """

        return 'SnailfishNumber([{left}, {right}])'.format(**self.__dict__)

    @staticmethod
    def add_to_left(pair, value):
        while pair.is_left:
            pair = pair.parent
            if pair is None:
                return

        if pair.parent is None:
            return

        pair = pair.parent

        if isinstance(pair.left, int):
            pair.left += value
            return

        pair = pair.left

        while not isinstance(pair.right, int):
            pair = pair.right

        pair.right += value

    @staticmethod
    def add_to_right(pair, value):
        while not pair.is_left:
            pair = pair.parent
            if pair is None:
                return

        if pair.parent is None:
            return

        pair = pair.parent

        if isinstance(pair.right, int):
            pair.right += value
            return

        pair = pair.right

        while not isinstance(pair.left, int):
            pair = pair.left

        pair.left += value

    def explode(self):
        """
        >>> zero = SnailfishNumber([[[[0,7],4],[[7,8],[6,0]]],[8,1]])
        >>> zero.explode()
        False
        >>> one = SnailfishNumber([[[[[9, 8], 1], 2], 3], 4])
        >>> one.explode()
        True
        >>> one
        SnailfishNumber([[[[0, 9], 2], 3], 4])
        >>> two = SnailfishNumber([7, [6, [5, [4, [3, 2]]]]])
        >>> two.explode()
        True
        >>> two
        SnailfishNumber([7, [6, [5, [7, 0]]]])
        >>> three = SnailfishNumber([[6,[5,[4,[3,2]]]],1])
        >>> three.explode()
        True
        >>> three
        SnailfishNumber([[6, [5, [7, 0]]], 3])
        >>> four = SnailfishNumber([[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]])
        >>> four.explode()
        True
        >>> four
        SnailfishNumber([[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]])
        >>> four.explode()
        True
        >>> four
        SnailfishNumber([[3, [2, [8, 0]]], [9, [5, [7, 0]]]])
        >>> four.explode()
        False
        >>> five = SnailfishNumber([[[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1]])
        >>> five.explode()
        True
        >>> five
        SnailfishNumber([[[[0, 7], 4], [7, [[8, 4], 9]]], [1, 1]])
        >>> six = SnailfishNumber([
        ...     [[[4, 0], [5, 0]], [[[4, 5], [2, 6]], [9, 5]]], [7, [[[3, 7], [4, 3]], [[6, 3], [8, 8]]]]
        ... ])
        >>> six.explode()
        True
        >>> six
        SnailfishNumber([[[[4, 0], [5, 4]], [[0, [7, 6]], [9, 5]]], [7, [[[3, 7], [4, 3]], [[6, 3], [8, 8]]]]])
        """

        stack = [(self, 1)]

        while stack:
            value, depth = stack.pop()

            if not isinstance(value, SnailfishNumber):
                continue

            if depth > 4:
                SnailfishNumber.add_to_left(value, value.left)
                SnailfishNumber.add_to_right(value, value.right)

                if value.is_left:
                    value.parent.left = 0
                else:
                    value.parent.right = 0

                return True

            stack.append((value.right, depth + 1))
            stack.append((value.left, depth + 1))

        return False

    def split(self):
        """
        >>> one = SnailfishNumber([[[[0, 7], 4], [15, [0, 13]]], [1, 1]])
        >>> one.split()
        True
        >>> one
        SnailfishNumber([[[[0, 7], 4], [[7, 8], [0, 13]]], [1, 1]])
        >>> one.split()
        True
        >>> one
        SnailfishNumber([[[[0, 7], 4], [[7, 8], [0, [6, 7]]]], [1, 1]])
        >>> one.split()
        False
        """

        stack = [(self, self.is_left, self.parent)]

        while stack:
            value, is_left, parent = stack.pop()

            if isinstance(value, int):
                if value >= 10:
                    split_left = value // 2
                    split_right = split_left + (value % 2 > 0)
                    split = SnailfishNumber(is_left=is_left, left=split_left, right=split_right)
                    split.parent = parent

                    if is_left:
                        parent.left = split
                    else:
                        parent.right = split
                    return True

                continue

            stack.append((value.right, False, value))
            stack.append((value.left, True, value))

        return False

    def reduce(self):
        """
        >>> one = SnailfishNumber([[[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1]])
        >>> one.reduce()
        >>> one
        SnailfishNumber([[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]])
        >>> two = SnailfishNumber([[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]], [7,[[[3,7],[4,3]],[[6,3],[8,8]]]]])
        >>> two.reduce()
        >>> two
        SnailfishNumber([[[[4, 0], [5, 4]], [[7, 7], [6, 0]]], [[8, [7, 7]], [[7, 9], [5, 0]]]])
        >>> three = SnailfishNumber([
        ...     [[[[7, 0], [7, 7]], [[7, 7], [7, 8]]], [[[7, 7], [8, 8]], [[7, 7], [8, 7]]]], [7, [5, [[3, 8], [1, 4]]]]
        ... ])
        >>> three.reduce()
        >>> three
        SnailfishNumber([[[[7, 7], [7, 8]], [[9, 5], [8, 7]]], [[[6, 8], [0, 8]], [[9, 9], [9, 0]]]])
        """

        while True:

            if self.explode():
                continue

            if self.split():
                continue

            break

    def copy(self):
        return SnailfishNumber(f'{self}')

    def __add__(self, other):
        """
        >>> SnailfishNumber([[[[4, 3], 4], 4], [7, [[8, 4], 9]]]) + SnailfishNumber([1, 1])
        SnailfishNumber([[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]])
        >>> SnailfishNumber([[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]) + \\
        ...     SnailfishNumber([7,[[[3,7],[4,3]],[[6,3],[8,8]]]])
        SnailfishNumber([[[[4, 0], [5, 4]], [[7, 7], [6, 0]]], [[8, [7, 7]], [[7, 9], [5, 0]]]])
        >>> SnailfishNumber([[[[7, 0], [7, 7]], [[7, 7], [7, 8]]], [[[7, 7], [8, 8]], [[7, 7], [8, 7]]]]) + \\
        ...     SnailfishNumber([7, [5, [[3, 8], [1, 4]]]])
        SnailfishNumber([[[[7, 7], [7, 8]], [[9, 5], [8, 7]]], [[[6, 8], [0, 8]], [[9, 9], [9, 0]]]])
        """

        result = SnailfishNumber(left=self.copy(), right=other.copy())
        result.reduce()
        return result

    def magnitude(self):
        """
        >>> SnailfishNumber([9, 1]).magnitude()
        29
        >>> SnailfishNumber([[[[0,7],4],[[7,8],[6,0]]],[8,1]]).magnitude()
        1384
        >>> SnailfishNumber([[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]).magnitude()
        3488
        """

        left_mag = self.left if isinstance(self.left, int) else self.left.magnitude()
        right_mag = self.right if isinstance(self.right, int) else self.right.magnitude()
        return 3 * left_mag + 2 * right_mag


def part1(data):
    """
    >>> three = [
    ...     SnailfishNumber([[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]),
    ...     SnailfishNumber([[[5,[2,8]],4],[5,[[9,9],0]]]),
    ...     SnailfishNumber([6,[[[6,2],[5,6]],[[7,6],[4,7]]]]),
    ...     SnailfishNumber([[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]),
    ...     SnailfishNumber([[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]),
    ...     SnailfishNumber([[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]),
    ...     SnailfishNumber([[[[5,4],[7,7]],8],[[8,3],8]]),
    ...     SnailfishNumber([[9,3],[[9,9],[6,[4,9]]]]),
    ...     SnailfishNumber([[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]),
    ...     SnailfishNumber([[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]])
    ... ]
    >>> part1(three)
    4140

    >>> part1(read_input())
    3869
    """

    result = data[0]

    for number in data[1:]:
        result = result + number

    return result.magnitude()


def part2(data):
    """
    >>> part2(read_input())
    4671
    """

    return max((a + b).magnitude() for a, b in permutations(data, 2))


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
