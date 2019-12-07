import itertools

START, END = 124075, 580769


def get_grouped_values_list(increasing_values):
    grouped_values = []
    for value in increasing_values:
        grouped_values.append([len(list(g)) for k, g in itertools.groupby(value)])
    return grouped_values


def get_increasing_values():
    increasing_numbers = []
    for n in range(START, END + 1):
        n_str = str(n)
        if list(n_str) != sorted(n_str):
            continue
        increasing_numbers.append(n_str)
    return increasing_numbers


def solve_part_a(grouped_values_list):
    counter = 0

    for grouped_values in grouped_values_list:
        counter += any(value >= 2 for value in grouped_values)
    return counter


def solve_part_b(grouped_values_list):
    counter = 0
    for grouped_values in grouped_values_list:
        counter += any(value == 2 for value in grouped_values)
    return counter


def main():
    increasing_values = get_increasing_values()
    grouped_values_list = get_grouped_values_list(increasing_values)

    solution_part_a: int = solve_part_a(grouped_values_list)
    print(f"Solution part A is: {solution_part_a}")

    solution_part_b: int = solve_part_b(grouped_values_list)
    print(f"Solution part B is: {solution_part_b}")


if __name__ == "__main__":
    main()
