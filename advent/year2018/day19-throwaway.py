import re

POINTER_PATTERN = re.compile(r"#ip (\d)")
INSTRUCTION_PATTERN = re.compile(r"([a-z]{4}) (\d+) (\d+) (\d+)")


def read_input():
    file = open('input/2018/day19-input.txt', 'r')
    text = file.read()
    
    match = POINTER_PATTERN.match(text)
    register = int(match.group(1))

    instructions = []

    for groups in INSTRUCTION_PATTERN.findall(text):
        instructions.append([groups[0]] + [int(i) for i in groups[1:4]])

    return (register, instructions)


def rewrite():
    (_, instructions) = read_input()
    
    IF_PATTERN = re.compile(
        r"if (.*) then e = 1 else e = 0\n"
        r"skip e\n"
        r"(.*)\n"
    )

    names = ['a', 'b', 'c', 'd', 'i', 'e']
    commands = []

    for (line, (op, a, b, c)) in enumerate(instructions):
        c = names[c]

        if op == "addr":
            a = names[a]

            if a == "i":
                a = line

            b = names[b]
            
            if b == "i":
                b = line

            if c == "i":                 
                if str(a) > str(b):
                    (a, b) = (b, a)

                command = "goto {} + {}".format(a, b)
            else:    
                command = "{} = {} + {}".format(c, a, b)            
        
        elif op == "addi":
            a = names[a]
            if c == "i": 
                b = b + line + 1
                command = "goto {}".format(b)
            else:    
                command = "{} = {} + {}".format(c, a, b)            
        
        elif op == "mulr":
            a = names[a]
            b = names[b]

            if a == "i":
                a = line

            if b == "i":
                b = line

            if a == "i" and b == "i" and c == "i":
                delta = line * line + 1
                command = "goto {}".format(delta)
            else:
                command = "{} = {} * {}".format(c, a, b)            
        elif op == "muli":
            a = names[a]
            command = "{} = {} * {}".format(c, a, b)
        elif op == "seti":
            if c == "i":
                a += 1
                command = "goto {}".format(a)
            else:
                command = "{} = {}".format(c, a)
        elif op == "setr":
            a = names[a]

            if a == "i":
                a = line

            command = "{} = {}".format(c, a)
        elif op == "eqrr":
            a = names[a]
            b = names[b]
            command = "if {} == {} then {} = 1 else {} = 0".format(a, b, c, c)
        elif op == "gtrr":
            a = names[a]
            b = names[b]
            command = "if {} > {} then {} = 1 else {} = 0".format(a, b, c, c)

        commands.append(command)

    labels = {}
    words = ['apple', 'banana', 'carrot', 'doggo', 'eggs', 'fruit', 'guava']
    index = 0

    for line, command in enumerate(commands):
        tmp = command.split()

        if len(tmp) == 2 and tmp[0] == 'goto':

            goto = int(tmp[1])

            label = labels.get(goto)

            if label is None:
                label = words[index]
                index += 1
                labels[goto] = label

            commands[line] = "goto {}".format(label)

        if command.startswith("goto {} + ".format(line)):
            commands[line] = "skip {}".format(command.split()[3])

    output = []

    for line, command in enumerate(commands):
        label = labels.get(line)
        label = "" if label is None else label + ":\n"
        output.append("{}{}".format(label, command))

    output = "\n".join(output)
    
    output = IF_PATTERN.sub(r"if not (\1) then \2\n", output)
    
    print(output)


def main():
    rewrite()


if __name__ == "__main__":
    main()
