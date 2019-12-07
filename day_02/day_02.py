import itertools
from typing import List

ADD = 1
MULTIPLY = 2
EXIT = 99


def get_program() -> List[int]:
    with open("input.txt") as f:
        program_str_list = f.readline().split(",")
        return list(map(int, program_str_list))


def replace_program_values(program: List[int], val_1: int, val_2: int):
    program[1] = val_1
    program[2] = val_2


def instruction_add(program: List[int], a_index: int, b_index: int, store_index: int):
    program[store_index] = program[a_index] + program[b_index]


def instruction_multiply(
    program: List[int], a_index: int, b_index: int, store_index: int
):
    program[store_index] = program[a_index] * program[b_index]


def instruction_exit_program(*_):
    raise StopIteration()


def eval_instruction(index: int, program: List[int]):
    instruction, *variables = program[0 + index : 4 + index]
    instructions = {
        ADD: instruction_add,
        MULTIPLY: instruction_multiply,
        EXIT: instruction_exit_program,
    }
    instructions[instruction](program, *variables)


def run_program(program: List[int]):
    index: int = 0
    while True:
        try:
            eval_instruction(index, program)
            index += 4
        except StopIteration:
            break


def solve_part_a():
    program: List[int] = get_program()
    replace_program_values(program, 12, 2)
    run_program(program)
    return program[0]


def solve_part_b():
    for noun, verb in itertools.product(range(100), range(100)):
        program: List[int] = get_program()
        replace_program_values(program, noun, verb)
        run_program(program)

        if program[0] == 19690720:
            return 100 * noun + verb


def main():
    solution_part_a: int = solve_part_a()
    print(f"Solution part A is: {solution_part_a}")

    solution_part_b: int = solve_part_b()
    print(f"Solution part B is: {solution_part_b}")


if __name__ == "__main__":
    main()
