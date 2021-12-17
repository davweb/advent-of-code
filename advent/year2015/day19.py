# -*- coding: utf-8 -*-

import re
import string

PATTERN = re.compile(r'(\w+) => (\w+)')


def read_input():

    with open('input/2015/day19-input.txt') as file:
        substitutions = []

        while True:
            line = file.readline()
            match = PATTERN.match(line)

            if match:
                substitutions.append(match.group(1, 2))
            else:
                break

        formula = file.readline()
        return (substitutions, formula)


def find_all(needle, haystack):
    index = 0

    while True:
        index = haystack.find(needle, index)

        if index == -1:
            return

        yield index
        index += len(needle)


def part1(data):
    """
    >>> part1(read_input())
    509
    """

    molecules = set()

    substitutions, formula = data

    for before, after in substitutions:
        for index in find_all(before, formula):
            new_molecule = formula[:index] + after + formula[index + len(before):]
            molecules.add(new_molecule)

    return len(molecules)



def elements(substitutions):
    """
    >>> sorted(elements((('Al', 'ThF'), ('Al', 'ThRnFAr'))))
    ['Al', 'Ar', 'F', 'Rn', 'Th']
    """

    elements = set()
    after_elements = set()

    for before, after in substitutions:
        elements.add(before)
        element = ''

        for c in after:
            if c in string.ascii_uppercase and element != '':
                elements.add(element)
                after_elements.add(element)
                element = ''
            
            element += c
            
        if element != '':
            elements.add(element)
            after_elements.add(element)
    
    return elements - after_elements

 

def reverse(substitutions, molecule, steps=0, state=None):
    """
    >>> reverse((('e', 'H'), ('e', 'O'), ('H', 'HO'), ('H', 'OH'), ('O', 'HH')), 'HOH')
    3
    >>> reverse((('e', 'H'), ('e', 'O'), ('H', 'HO'), ('H', 'OH'), ('O', 'HH')), 'HOHOHO')
    6
    """

    if state is None:
        state = {
            'shortest': len(molecule),
            'best': None,
            'seen': {}
        }

    if molecule in state['seen'] and state['seen'][molecule] <= steps:
        return

    state['seen'][molecule] = steps

    if state['shortest'] is None or len(molecule) < state['shortest']:
        state['shortest'] = len(molecule)
        print(state['shortest'])

    if molecule == 'e':
        if state['best'] is None or steps < state['best']:
            state['best'] = steps

        return state['best']

    for before, after in substitutions:
        for index in find_all(after, molecule):
            new_molecule = molecule[:index] + before + molecule[index + len(after):]

            if 'e' in molecule and len(molecule) > 1:
                continue
            reverse(substitutions, new_molecule, steps + 1, state)

    return state['best']




def part2(data):
    """
    # >>> part2(read_input())
    # 0
    """

    substitutions, formula = data
    return reverse(substitutions, formula)


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
