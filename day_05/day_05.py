from typing import List

OPCODE_ADD = "01"
OPCODE_MULTIPLY = "02"
OPCODE_INPUT = "03"
OPCODE_OUTPUT = "04"
OPCODE_JT = "05"
OPCODE_JF = "06"
OPCODE_LESS_THAN = "07"
OPCODE_EQUAL = "08"
OPCODE_EXIT = "99"
PARAMETER_MODE_POSITION = "0"
PARAMETER_MODE_IMMEDIATE = "1"


class Interpreter:
    def __init__(self, program, program_input):
        self.index = 0
        self.mode = 0
        self.program = program
        self.input = program_input
        self.output = []
        self.parameter_modes = ""

    def run(self):
        while True:
            try:
                self._eval_instruction()
            except StopIteration:
                break

    def _eval_instruction(self):
        instruction, *variables = self.program[0 + self.index : 4 + self.index]
        instruction = str(instruction).zfill(6)
        self.parameter_modes, instruction = instruction[:-2][::-1], instruction[-2:]

        instructions = {
            OPCODE_ADD: self._instruction_add,
            OPCODE_MULTIPLY: self._instruction_multiply,
            OPCODE_INPUT: self._instruction_input,
            OPCODE_OUTPUT: self._instruction_output,
            OPCODE_EXIT: self._instruction_exit,
            OPCODE_JT: self._instruction_jump_if_true,
            OPCODE_JF: self._instruction_jump_if_false,
            OPCODE_LESS_THAN: self._instruction_less_than,
            OPCODE_EQUAL: self._instruction_equal,
        }
        return instructions[instruction](*variables)

    def _get(self, value, position: int):
        if self.parameter_modes[position] == PARAMETER_MODE_IMMEDIATE:
            return value
        return self.program[value]

    def _instruction_add(self, a: int, b: int, store: int):
        self.program[store] = self._get(a, 0) + self._get(b, 1)
        self.index += 4

    def _instruction_multiply(self, a: int, b: int, store: int):
        self.program[store] = self._get(a, 0) * self._get(b, 1)
        self.index += 4

    def _instruction_input(self, store, *_):
        self.program[store] = self.input.pop()
        self.index += 2

    def _instruction_output(self, value, *_):
        self.output.append(self._get(value, 0))
        self.index += 2

    def _instruction_jump_if_true(self, comp, a, *_):
        if self._get(comp, 0) != 0:
            self.index = self._get(a, 1)
        else:
            self.index += 3

    def _instruction_jump_if_false(self, comp, a, *_):
        if self._get(comp, 0) == 0:
            self.index = self._get(a, 1)
        else:
            self.index += 3

    def _instruction_less_than(self, a, b, store, *_):
        self.program[store] = int(self._get(a, 0) < self._get(b, 1))
        self.index += 4

    def _instruction_equal(self, a, b, store, *_):
        self.program[store] = int(self._get(a, 0) == self._get(b, 1))
        self.index += 4

    def _instruction_exit(self, *_):
        raise StopIteration()


def get_program() -> List[int]:
    with open("input.txt") as f:
        program_str_list = f.readline().split(",")
        return list(map(int, program_str_list))


def solve(initial_input):
    program: List[int] = get_program()
    interpreter = Interpreter(program, [initial_input])
    interpreter.run()
    return interpreter.output[-1]


def main():
    solution_part_a: int = solve(1)
    print(f"Solution part A is: {solution_part_a}")

    solution_part_b: int = solve(5)
    print(f"Solution part B is: {solution_part_b}")


if __name__ == "__main__":
    main()
