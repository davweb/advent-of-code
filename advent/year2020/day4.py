#!/usr/local/bin/python3

import re
from itertools import chain

REQUIRED = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}
HCL_PATTERN = re.compile(r"^#[0-9a-f]{6}$")
ECL_SET = {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}
PID_PATTERN = re.compile(r"^\d{9}$")
HGT_PATTERN = re.compile(r"^(\d+)(cm|in)$")


def read_input():
    file = open('input/2020/day4-input.txt', 'r')
    passports = []
    passport = []

    for line in chain(file, ['']):
        line = line.strip()

        if line == '':
            passports.append(dict(item.split(':') for item in passport))
            passport = []
        else:
            passport.extend(line.split())

    return passports


def is_valid(passport):
    """
    >>> is_valid({
    ...     'ecl': 'gry', 'pid': '860033327', 'eyr': '2020', 'hcl': '#fffffd', 'byr': '1937', 
    ...     'iyr': '2017', 'cid': '147', 'hgt': '183cm'
    ... })
    True
    >>> is_valid({
    ...    'iyr': '2013', 'ecl': 'amb', 'cid': '350', 'eyr': '2023', 'pid': '028048884',
    ...     'hcl': '#cfa07d', 'byr': '1929'
    ... })
    False
    >>> is_valid({
    ...     'hcl': '#ae17e1', 'iyr': '2013', 'eyr': '2024',
    ...     'ecl': 'brn', 'pid': '760753108', 'byr': '1931', 'hgt': '179cm'
    ... })
    True
    """

    return set(passport.keys()).intersection(REQUIRED) == REQUIRED


def is_completely_valid(passport):
    """
    >>> is_completely_valid({
    ...     'ecl': 'gry', 'pid': '860033327', 'eyr': '2020', 'hcl': '#fffffd', 'byr': '1937', 
    ...     'iyr': '2017', 'cid': '147', 'hgt': '183cm'
    ... })
    True
    >>> is_completely_valid({
    ...    'iyr': '2013', 'ecl': 'amb', 'cid': '350', 'eyr': '2023', 'pid': '028048884',
    ...     'hcl': '#cfa07d', 'byr': '1929'
    ... })
    False
    >>> is_completely_valid({
    ...     'hcl': '#ae17e1', 'iyr': '2013', 'eyr': '2024',
    ...     'ecl': 'brn', 'pid': '760753108', 'byr': '1931', 'hgt': '179cm'
    ... })
    True
    >>> is_completely_valid({
    ...     'ecl': 'teal', 'pid': '860033327', 'eyr': '2020', 'hcl': '#fffffd', 'byr': '1937', 
    ...     'iyr': '2017', 'cid': '147', 'hgt': '183cm'
    ... })
    False
    >>> is_completely_valid({
    ...     'ecl': 'gry', 'pid': '860033327', 'eyr': '2020', 'hcl': '#fffffd', 'byr': '1937', 
    ...     'iyr': '2017', 'cid': '147', 'hgt': '83cm'
    ... })
    False
    """

    try:    
        byr = int(passport['byr'])
        iyr = int(passport['iyr'])
        eyr = int(passport['eyr'])
        hgt = passport['hgt']
        hcl = passport['hcl']
        ecl = passport['ecl']
        pid = passport['pid']
    except KeyError:
        return False

    if not 1920 <= byr <= 2002:
        return False
    
    if not 2010 <= iyr <= 2020:
        return False

    if not 2020 <= eyr <= 2030:
        return False

    height_match = HGT_PATTERN.match(hgt)

    if not height_match:
        return False

    height = int(height_match.group(1))
    height_unit = height_match.group(2)

    if height_unit == 'cm' and not 150 <= height <= 193:
        return False

    if height_unit == 'in' and not 59 <= height <= 76:
        return False

    if not HCL_PATTERN.match(hcl):
        return False

    if not ecl in ECL_SET:
        return False

    if not PID_PATTERN.match(pid):
        return False

    return True


def part1(data):
    """
    >>> part1(read_input())
    192
    """
    
    return sum(is_valid(passport) for passport in data)


def part2(data):
    """
    >>> part2(read_input())
    101
    """
    
    return sum(is_completely_valid(passport) for passport in data)


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
