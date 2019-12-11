import hashlib

def bounds(points):
    """
    >>> bounds([(0, 0)])
    ((0, 0), (0, 0))
    >>> bounds([(7, 1), (-1, 9)])
    ((-1, 1), (7, 9))
    """

    left = min(x for (x,y) in points)
    right = max(x for (x,y) in points)
    top = min(y for (x,y) in points)
    bottom = max(y for (x,y) in points)
    
    return ((left, top), (right, bottom))

def md5(string):
    """
    >>> md5("test")
    '098f6bcd4621d373cade4e832627b4f6'
    """
    
    return hashlib.md5(string.encode('utf-8')).hexdigest()