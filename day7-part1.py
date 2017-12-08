import re

pattern = re.compile("([a-z]+) \((\d+)\)( -> ([a-z, ]+))?")
supported = set()
names = set()

for line in file("day7-input.txt"):
    result = pattern.match(line)
    name, weight, supporting = result.group(1, 2, 4)
    names.add(name)
    if supporting is not None:
        supported.update(supporting.split(', '))

print (names - supported).pop()