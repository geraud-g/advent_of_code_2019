from itertools import permutations
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
AMPLIFIERS = 5


class StopFeedbackLoopException(StopIteration):
    pass


class Interpreter:
    def __init__(self, program, program_input, part=1):
        self.index = 0
        self.mode = 0
        self.program = program
        self.input = program_input
        self.output = []
        self.parameter_modes = ""
        self.part = part

    def run(self):
        while True:
            try:
                self._eval_instruction()
            except StopIteration as e:
                if type(e) == StopFeedbackLoopException:
                    raise StopFeedbackLoopException()
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
        self.program[store] = self.input.pop(0)
        self.index += 2

    def _instruction_output(self, value, *_):
        self.output.append(self._get(value, 0))
        self.index += 2
        if self.part == 2:
            raise StopIteration()

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
        if self.part == 2:
            raise StopFeedbackLoopException()
        raise StopIteration()


def get_program() -> List[int]:
    with open("input.txt") as f:
        program_str_list = f.readline().split(",")
        return list(map(int, program_str_list))


def try_phase_settings(phase_settings, initial_input):
    last_input = initial_input

    for phase_setting in phase_settings:
        program: List[int] = get_program()
        interpreter = Interpreter(program, [phase_setting, last_input])
        interpreter.run()
        last_input = interpreter.output[-1]
    return last_input


def try_phase_settings_part_b(phase_settings, initial_input):
    last_input = initial_input
    interpreters = [Interpreter(get_program(), [ps], part=2) for ps in phase_settings]

    while True:
        try:
            for interpreter in interpreters:
                interpreter.input.append(last_input)
                interpreter.run()
                last_input = interpreter.output[-1]
        except StopFeedbackLoopException:
            break
    return interpreters[-1].output[-1]


def solve_part_a():
    possible_phase_settings = permutations([0, 1, 2, 3, 4])
    outputs = []
    for phase_settings in possible_phase_settings:
        output = try_phase_settings(phase_settings, 0)
        outputs.append(output)
    return max(outputs)


def solve_part_b():
    possible_phase_settings = permutations([5, 6, 7, 8, 9])
    outputs = []
    for phase_settings in possible_phase_settings:
        output = try_phase_settings_part_b(phase_settings, 0)
        outputs.append(output)
    return max(outputs)


def main():
    solution_part_a: int = solve_part_a()
    print(f"Solution part A is: {solution_part_a}")

    solution_part_b: int = solve_part_b()
    print(f"Solution part B is: {solution_part_b}")


if __name__ == "__main__":
    main()
