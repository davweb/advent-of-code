# -*- coding: utf-8 -*-

def read_input():
    with open('input/2022/day7-input.txt', encoding='utf8') as file:
        return [line.strip() for line in file.readlines()]


class Dir:
    def __init__(self, parent):
        self.parent = parent
        self.size = 0
        self.children = []

        if parent is not None:
            parent.add_child(self)

    def add_file(self, filesize):
        self.size += filesize

    def add_child(self, child):
        self.children.append(child)

    def recursive_size(self):
        return self.size + sum(child.recursive_size() for child in self.children)


def read_listing(data):

    for line in data:

        match line.split():
            case '$', 'cd', '/':
                root = Dir(None)
                all_directories = [root]
                stack = [root]
            case '$', 'cd', '..':
                stack.pop()
            case '$', 'cd', _:
                directory = Dir(stack[-1])
                all_directories.append(directory)
                stack.append(directory)
            case '$', 'ls':
                pass
            case 'dir', _:
                pass
            case filesize, _:
                stack[-1].add_file(int(filesize))

    return all_directories


def part1(data):
    """
    >>> part1(read_input())
    1886043
    """

    dirs = read_listing(data)
    return sum(x.recursive_size() for x in dirs if x.recursive_size() <= 100000)


def part2(data):
    """
    >>> part2(read_input())
    3842121
    """

    DISK_SPACE = 70000000
    NEEDED = 30000000

    dirs = read_listing(data)

    used = dirs[0].recursive_size()
    free = DISK_SPACE - used
    to_delete = NEEDED - free

    return min(x.recursive_size() for x in dirs if x.recursive_size() >= to_delete)


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
