from enum import IntEnum

class OpCode(IntEnum):
    ADD = 1
    MULTIPLY = 2
    SAVE = 3
    OUTPUT = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESS_THAN = 7
    EQUAL_TO = 8
    EXIT = 99

class IntCode:
    
    def __init__(self, memory, input=None):
        self.memory = memory.copy()
        self.input = [] if input is None else input
        self.index = 0

    def generate_parameter_modes(self, op_code):
        """
        >>> i = IntCode([])
        >>> pm = i.generate_parameter_modes(3)
        >>> [next(pm), next(pm)]
        [0, 0]
        >>> pm = i.generate_parameter_modes(7200103)
        >>> [next(pm), next(pm), next(pm), next(pm), next(pm), next(pm)]
        [1, 0, 0, 2, 7, 0]
        """

        modes = op_code // 100

        while modes > 0:
            yield modes % 10
            modes //= 10
        
        while True:
            yield 0

    def next_instruction(self):
        """
        >>> i = IntCode([1])
        >>> i.next_instruction()
        1
        >>> i = IntCode([101])
        >>> i.next_instruction()
        1
        """

        instruction = self.memory[self.index]
        self.index += 1
        self.parameter_modes = self.generate_parameter_modes(instruction)
        return instruction % 100

    def get_next_parameter(self):
        """
        >>> i = IntCode([1, 2, 99])
        >>> n = i.next_instruction()
        >>> i.get_next_parameter()
        99
        >>> i= IntCode([101, 2, 99])
        >>> n = i.next_instruction()
        >>> i.get_next_parameter()
        2
        """
        parameter_value = self.memory[self.index]
        self.index += 1
        parameter_mode = next(self.parameter_modes)

        # position mode   
        if parameter_mode == 0:
            return self.memory[parameter_value]
        # immediate mode    
        elif parameter_mode == 1:
            return parameter_value
        else:
            raise ValueError("Invalid parameter mode '{}'".format(parameter_mode))
        
    def set_next_parameter(self, parameter_value):
        destination_index = self.memory[self.index]
        self.index += 1
        parameter_mode = next(self.parameter_modes)

        # position mode   
        if parameter_mode == 0:
            self.memory[destination_index] = parameter_value
        else:
            raise ValueError("Invalid parameter mode '{}'".format(parameter_mode)) 

    def next_input(self):
        """"
        >>> i = IntCode([])
        >>> i.input = [1, 2]
        >>> i.next_input()
        1
        >>> i.next_input()
        2
        """
        try:
            return self.input.pop(0)
        except IndexError:
            raise ValueError("Not enough input values")

    def execute(self, input=None):
        """
        >>> IntCode([87]).execute([])
        Traceback (most recent call last):
            ...
        ValueError: Invalid op code '87'
        >>> IntCode([1, 0, 0, 0, 4, 0, 99]).execute([])
        2
        >>> IntCode([2, 3, 0, 3, 4, 3, 99]).execute([])
        6
        >>> IntCode([2, 6, 6, 7, 4, 7, 99, 0]).execute([])
        9801
        >>> IntCode([1, 1, 1, 4, 99, 5, 6, 0, 4, 0, 99]).execute([])
        30
        >>> IntCode([3, 5, 4, 5, 99, -1]).execute([7])
        7
        >>> IntCode([1002, 8, 3, 7, 4, 7, 99, 4, 33]).execute([])
        99
        >>> IntCode([1105, 1, 4, 99, 4, 0, 99]).execute([])
        1105
        >>> IntCode([1106, 0, 4, 99, 4, 0, 99]).execute()
        1106
        >>> IntCode([1107, 1, 2, 7, 4, 7,99, 53]).execute()
        1
        >>> IntCode([1107, 2, 1, 7, 4, 7,99, 53]).execute()
        0
        >>> IntCode([1108, 1, 1, 7, 4, 7,99, 53]).execute()
        1
        >>> IntCode([1108, 2, 1, 7, 4, 7,99, 53]).execute()
        0
        >>> IntCode([3,3,1105,-1,9,1101,0,0,12,4,12,99,1]).execute([0])
        0
        >>> IntCode([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]).execute([1000])
        1
        >>> IntCode([3,3,1105,-1,9,1101,0,0,12,4,12,99,1]).execute([0])
        0
        >>> IntCode([3,3,1105,-1,9,1101,0,0,12,4,12,99,1]).execute([1000])
        1
        """
        if input is not None:
            self.input += input

        while True:
            op_code = self.next_instruction()

            if op_code == OpCode.ADD:
                left = self.get_next_parameter()
                right = self.get_next_parameter()
                self.set_next_parameter(left + right)

            elif op_code ==  OpCode.MULTIPLY:
                left = self.get_next_parameter()
                right = self.get_next_parameter()
                self.set_next_parameter(left * right)

            elif op_code ==  OpCode.SAVE:
                value = self.next_input()
                self.set_next_parameter(value)

            elif op_code == OpCode.OUTPUT:
                return self.get_next_parameter()

            elif op_code == OpCode.JUMP_IF_TRUE:
                conditional = self.get_next_parameter()
                destination_index = self.get_next_parameter()

                if conditional != 0:
                    self.index = destination_index

            elif op_code ==  OpCode.JUMP_IF_FALSE:
                conditional = self.get_next_parameter()
                destination_index = self.get_next_parameter()

                if conditional == 0:
                    self.index = destination_index

            elif op_code ==  OpCode.LESS_THAN:
                first = self.get_next_parameter()
                second = self.get_next_parameter()
                self.set_next_parameter(int(first < second))
            
            elif op_code == OpCode.EQUAL_TO:
                first = self.get_next_parameter()
                second = self.get_next_parameter()
                self.set_next_parameter(int(first == second))

            elif op_code == OpCode.EXIT:
                return None

            else:
                raise ValueError("Invalid op code '{}'".format(op_code))
