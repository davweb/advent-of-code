from collections import defaultdict

def parse_input(data):
    instructions = []

    for line in data:
        line = line.strip().split(" ")
        command = line[0]
        x = line[1]

        if command in ['snd', 'rcv']:
            y = None
        elif command in ['set', 'add', 'mul', 'mod', 'jgz']:
            y = line[2]
        else:
            raise Exception("Unknown instruction: {}".format(command))

        instructions.append((command, x, y))

    return instructions

def register_value(registers, value):
    if value is None:
        return None

    try:
        return int(value)
    except ValueError:
        return registers[value]

def part1(data):
    instructions = parse_input(data)
    registers = defaultdict(int)
    pointer = 0
    playing = None

    while pointer >= 0 and pointer < len(instructions):
        command, register, y = instructions[pointer]
        x = register_value(registers, register)
        y = register_value(registers, y)
        step = 1

        if command == "snd":
            playing = x
        elif command == "set":
            registers[register] = y
        elif command == "add":
            registers[register] = x + y
        elif command == "mul":
            registers[register] = x * y
        elif command == "mod":
            registers[register] = x % y
        elif command == "rcv":
            if x != 0:
                return playing
        elif command == "jgz":
            if x > 0:
                step = y
        else:
            raise Exception("Unknown instruction {}".format(command))

        pointer += step

    return None

def part2(data):
    instructions = parse_input(data)
    all_registers = [defaultdict(int), defaultdict(int)]
    all_pointers = [0,0]
    all_queues = [[], []]
    program = 0

    all_registers[0]['p'] = 0
    all_registers[1]['p'] = 1

    first = True
    count = 0
    
    while sum(len(q) for q in all_queues) > 0 or first:
        registers = all_registers[program]
        pointer = all_pointers[program]
        queue = all_queues[program]
        other_queue = all_queues[1 - program]

        command, register, y = instructions[pointer]
        x = register_value(registers, register)
        y = register_value(registers, y)

        step = 1

        if command == "snd":
            first = False            
            other_queue.append(x)
            if program == 1:
                count += 1
        elif command == "set":
            registers[register] = y
        elif command == "add":
            registers[register] = x + y
        elif command == "mul":
            registers[register] = x * y
        elif command == "mod":
            registers[register] = x % y
        elif command == "rcv":
            if len(queue) == 0:
                program = 1 - program
                step = 0
            else:
                registers[register] = queue.pop(0)
        elif command == "jgz":
            if x > 0:
                step = y
        else:
            raise Exception("Unknown instruction {}".format(command))

        pointer += step
        all_pointers[program] += step

    return count




def main():
    print part1(file("day18-sample.txt"))
    print part1(file("day18-input.txt"))
    print part2(file("day18-sample2.txt"))
    print part2(file("day18-input.txt"))

if __name__ == "__main__":
    main()
