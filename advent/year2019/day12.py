#!/usr/local/bin/python3

import itertools
import numpy 

class Moon:
    def __init__(self, position, velocity=None):
        """
        >>> Moon((0, 0, 0))
        Moon(position=(0, 0, 0), velocity=(0, 0, 0))
        >>> Moon((1, 2, 3), (4, 5, 6))
        Moon(position=(1, 2, 3), velocity=(4, 5, 6))
        >>> Moon((1, 1))
        Moon(position=(1, 1), velocity=(0, 0))
        """

        self.position = position
        if velocity is None:
            self.velocity = tuple([0] * len(position))
        else:
            self.velocity = velocity


    def __repr__(self):
        return "Moon(position={0}, velocity={1})".format(self.position, self.velocity)


    def move(self):
        """
        >>> moon = Moon((1, 2, 3), (4, 5, 6))
        >>> moon.move()
        >>> moon
        Moon(position=(5, 7, 9), velocity=(4, 5, 6))
        """

        self.position = tuple(p + v for p,v in zip(self.position, self.velocity))


    def gravity(self, other):
        """
        >>> alpha = Moon((1, 2, 3))
        >>> beta = Moon((5, 2, 1))
        >>> alpha.gravity(beta)
        >>> alpha.velocity
        (1, 0, -1)
        >>> alpha.gravity(beta)
        >>> alpha.velocity
        (2, 0, -2)
        """

        self.velocity = tuple(self.velocity[i] + closer(self.position[i], other.position[i]) for i in range(0, len(self.velocity)))

    
    def potential_energy(self):
        """
        >>> Moon((-1, 2, 7)).potential_energy()
        10
        """
        
        return sum(abs(v) for v in self.position)

    def kinetic_energy(self):
        """
        >>> Moon((-1, 2, 7), (-3, 8, 2)).kinetic_energy()
        13
        """
        
        return sum(abs(v) for v in self.velocity)

    def energy(self):
        return self.potential_energy() * self.kinetic_energy()


def closer(a, b):
    """
    >>> closer(1, 1)
    0
    >>> closer(1, 5)
    1
    >>> closer(-7, -11)
    -1
    >>> closer(5, 1)
    -1
    >>> closer(1, 2)
    1
    """

    if a > b:
        return -1
    elif a < b:
        return 1
    else:
        return 0
        

def simulate(moons, steps):
    """
    >>> tom = Moon((-1, 0, 2))
    >>> dick = Moon((2, -10, -7))
    >>> harry =  Moon((4, -8, 8))
    >>> george = Moon((3, 5, -1))
    >>> moons = [tom, dick, harry, george]
    >>> simulate(moons, 10)
    >>> tom
    Moon(position=(2, 1, -3), velocity=(-3, -2, 1))
    >>> dick
    Moon(position=(1, -8, 0), velocity=(-1, 1, 3))
    >>> harry
    Moon(position=(3, -6, 1), velocity=(3, 2, -3))
    >>> george
    Moon(position=(2, 0, 4), velocity=(1, -1, -1))
    """

    step = 0
    
    while step < steps:
        step += 1

        for (a,b) in itertools.combinations(moons, 2):
            a.gravity(b)
            b.gravity(a)

        for moon in moons:
            moon.move()


def part1(moons):
    """
    >>> part1(input_moons())
    6849
    """

    simulate(moons, 1000)
    return sum(moon.energy() for moon in moons)


def part2(moons):
    """
    >>> part2(input_moons())
    356658899375688
    """
    
    cycles = []

    for axis in range(0, 3):
        axis_moons = []
        cache = set()
        steps = 0
        
        for moon in moons:
            axis_moons.append(Moon((moon.position[axis],)))

        while True:
            cachekey = tuple((moon.position[0], moon.velocity[0]) for moon in axis_moons)

            if cachekey in cache:
                cycles.append(steps)
                break
            
            cache.add(cachekey)
            steps += 1
            simulate(axis_moons, 1)

    return numpy.lcm.reduce(cycles)


def input_moons():
    return [Moon((3, -6, 6)), Moon((10, 7, -9)), Moon((-3, -7, 9)), Moon((-8, 0, 4))]

def main():
    print(part1(input_moons()))
    print(part2(input_moons()))

if __name__ == "__main__":
    main()
