import re
from collections import defaultdict

pattern = re.compile("([a-z]+) (inc|dec) (-?\d+) if ([a-z]+) ([<>=!]+) (-?\d+)")
values = defaultdict(int)
maxval = None

for line in file('day8-input.txt'):
    result = pattern.match(line)
    target, op, amount, source, comparison, value = result.group(1, 2, 3, 4, 5, 6)
    amount = int(amount)
    value = int(value)
    current = values[source]
    
    if comparison == "==":
        result = current == value
    elif comparison == "!=":
        result = current != value
    elif comparison == ">":
        result = current > value
    elif comparison == "<":
        result = current < value
    elif comparison == ">=":
        result = current >= value
    elif comparison == "<=":
        result = current <= value
    else:
        raise ValueError("Unknown comparison: %s" % comparison)

    if result:
        old = values[target]
        
        if op == "inc":
            old += amount
        elif op == "dec":
            old -= amount    
        else:
            raise ValueError("Unknown operator: %s" % op)

        values[target] = old
        if maxval is None or maxval < old:
            maxval = old

print(max(values.values())), maxval