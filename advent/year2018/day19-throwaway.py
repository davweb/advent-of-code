import re

POINTER_PATTERN = re.compile(r"#ip (\d)")
INSTRUCTION_PATTERN = re.compile(r"([a-z]{4}) (\d+) (\d+) (\d+)")


def read_input():
    with open('input/2018/day19-input.txt', encoding='utf-8') as file:
        text = file.read()

    match = POINTER_PATTERN.match(text)
    register = int(match.group(1))

    instructions = []

    for groups in INSTRUCTION_PATTERN.findall(text):
        instructions.append([groups[0]] + [int(i) for i in groups[1:4]])

    return (register, instructions)


def generate_commands(instructions):
    names = ['a', 'b', 'c', 'd', 'i', 'e']
    commands = []

    for (line, (op, a, b, c)) in enumerate(instructions):
        c = names[c]

        match op:
            case "addr":
                a = line if names[a] == 'i' else names[a]
                b = line if names[b] == 'i' else names[b]

                if c == "i":
                    if str(a) > str(b):
                        (a, b) = (b, a)

                    command = f"goto {a} + {b}"
                else:
                    command = f"{c} = {a} + {b}"

            case "addi":
                a = names[a]
                if c == "i":
                    b = b + line + 1
                    command = f"goto {b}"
                else:
                    command = f"{c} = {a} + {b}"

            case "mulr":
                a = line if names[a] == 'i' else names[a]
                b = line if names[b] == 'i' else names[b]

                if a == "i" and b == "i" and c == "i":
                    delta = line * line + 1
                    command = f"goto {delta}"
                else:
                    command = f"{c} = {a} * {b}"

            case "muli":
                a = names[a]
                command = f"{c} = {a} * {b}"

            case "seti":
                if c == "i":
                    a += 1
                    command = f"goto {a}"
                else:
                    command = f"{c} = {a}"

            case "setr":
                a = names[a]

                if a == "i":
                    a = line

                command = f"{c} = {a}"

            case "eqrr":
                a = names[a]
                b = names[b]
                command = f"if {a} == {b} then {c} = 1 else {c} = 0"

            case "gtrr":
                a = names[a]
                b = names[b]
                command = f"if {a} > {b} then {c} = 1 else {c} = 0"

        commands.append(command)

    return commands


def rewrite():
    (_, instructions) = read_input()

    IF_PATTERN = re.compile(
        r"if (.*) then e = 1 else e = 0\n"
        r"skip e\n"
        r"(.*)\n"
    )

    commands = generate_commands(instructions)

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

            commands[line] = f"goto {label}"

        if command.startswith(f"goto {line} + "):
            commands[line] = f"skip {command.split()[3]}"

    output = []

    for line, command in enumerate(commands):
        label = labels.get(line)
        label = "" if label is None else label + ":\n"
        output.append(f"{label}{command}")

    output = "\n".join(output)

    output = IF_PATTERN.sub(r"if not (\1) then \2\n", output)

    print(output)


def main():
    rewrite()


if __name__ == "__main__":
    main()
