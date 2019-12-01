import math
from typing import List


def get_modules_masses() -> List[int]:
    with open("input.txt") as f:
        return list(map(int, f.readlines()))


def get_required_fuel(mass: int) -> int:
    return int(math.floor(mass / 3)) - 2


def get_required_fuel_part_b(mass: int) -> int:
    required_fuel = get_required_fuel(mass)
    if required_fuel <= 0:
        return 0
    return required_fuel + get_required_fuel_part_b(required_fuel)


def solve_part_a(modules_masses: List[int]) -> int:
    return sum(map(get_required_fuel, modules_masses))


def solve_part_b(modules_masses: List[int]) -> int:
    return sum(map(get_required_fuel_part_b, modules_masses))


def main():
    modules_masses = get_modules_masses()

    solution_part_a = solve_part_a(modules_masses)
    print(f"Solution part A is: {solution_part_a}")

    solution_part_b = solve_part_b(modules_masses)
    print(f"Solution part B is: {solution_part_b}")


if __name__ == "__main__":
    main()
