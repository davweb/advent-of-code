from _md5 import md5
import itertools

def mine(key, prefix):
 
    for count in itertools.count(start=1):
        message = "{}{}".format(key, count).encode('utf-8')
        hash = md5(message)
        digest = hash.hexdigest()

        if digest.startswith(prefix):
            return count


def part1(data):
    """
    >>> part1("abcdef")
    609043
    >>> part1("pqrstuv")
    1048970
    >>> part1("iwrupvqb")
    346386
    """

    return mine(data, "00000")


def part2(data):
    """
    >>> part2("iwrupvqb")
    9958218
    """
    
    return mine(data, "000000")


def main():
    data = "iwrupvqb"
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
