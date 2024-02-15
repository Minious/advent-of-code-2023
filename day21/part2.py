import math

dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def one_step(grid, positions):
    new_positions = set()
    for position in positions:
        for dir in dirs:
            new_position = tuple(map(lambda i, j: i + j, position, dir))
            if new_position[0] < 0 or new_position[1] < 0 or new_position[0] >= len(grid[0]) or new_position[1] >= len(grid):
                continue
            if grid[new_position[1]][new_position[0]] != "#":
                new_positions.add(new_position)
    return new_positions


def spread_from(grid, start, steps):
    positions = [start]
    for i in range(steps):
        positions = one_step(grid, (positions))
    return positions


if __name__ == '__main__':
    f = open("input.txt", "r")

    grid = [[c for c in line] for line in f.read().splitlines()]

    steps = 26501365
    start = [(line.index("S"), i)
             for i, line in enumerate(grid)
             if "S" in line][0]
    mid_length = int((len(grid) - 1) / 2)
    partial_square_diagonal_count = math.floor(steps / len(grid))
    full_square_quarter_count = partial_square_diagonal_count * \
        (partial_square_diagonal_count + 1) / 2
    full_square_count = int(full_square_quarter_count *
                            4 + (1 if steps > len(grid) else 0))
    full_square_count_max = partial_square_diagonal_count * partial_square_diagonal_count
    full_square_count_min = (
        partial_square_diagonal_count - 1) * (partial_square_diagonal_count - 1)

    tips_steps = (steps - mid_length) - \
        (partial_square_diagonal_count - 1) * len(grid) - 1

    print("tips_steps", tips_steps)
    print("full_square_mid_length_count",
          "(", steps, "-", mid_length, ")", "/", len(grid))
    print("partial_square_diagonal_count up", partial_square_diagonal_count)
    print("partial_square_diagonal_count down",
          partial_square_diagonal_count - 1)
    print("full_square_quarter_count", full_square_quarter_count)
    print("full_square_count", full_square_count)

    print("A")
    full_square_even_steps = len(grid) + len(grid) % 2
    full_square_positions_even = spread_from(
        grid, start, full_square_even_steps)
    full_square_positions_odd = spread_from(
        grid, start, full_square_even_steps + 1)

    print("B")
    double_hor_grid = [[grid[j % len(grid)][i % len(grid)] for i in range(len(grid) * 2)]
                       for j in range(len(grid))]
    double_vert_grid = [[grid[j % len(grid)][i % len(grid)] for i in range(len(grid))]
                        for j in range(len(grid) * 2)]
    left_tip_positions = spread_from(
        double_hor_grid, (len(grid[0]) * 2 - 1, start[1]), tips_steps)
    right_tip_positions = spread_from(
        double_hor_grid, (0, start[1]), tips_steps)
    top_tip_positions = spread_from(
        double_vert_grid, (start[0], len(grid) * 2 - 1), tips_steps)
    bottom_tip_positions = spread_from(
        double_vert_grid, (start[0], 0), tips_steps)

    print("C")
    diag_high_steps = steps - partial_square_diagonal_count * len(grid) - 1
    bottom_left_high_diag_positions = spread_from(
        grid, (len(grid[0]) - 1, 0), diag_high_steps)
    top_left_high_diag_positions = spread_from(
        grid, (len(grid[0]) - 1, len(grid) - 1), diag_high_steps)
    bottom_right_high_diag_positions = spread_from(
        grid, (0, 0), diag_high_steps)
    top_right_high_diag_positions = spread_from(
        grid, (0, len(grid) - 1), diag_high_steps)

    print("D")
    diag_low_steps = steps - \
        (partial_square_diagonal_count - 1) * len(grid) - 1
    bottom_left_low_diag_positions = spread_from(
        grid, (len(grid[0]) - 1, 0), diag_low_steps)
    top_left_low_diag_positions = spread_from(
        grid, (len(grid[0]) - 1, len(grid) - 1), diag_low_steps)
    bottom_right_low_diag_positions = spread_from(
        grid, (0, 0), diag_low_steps)
    top_right_low_diag_positions = spread_from(
        grid, (0, len(grid) - 1), diag_low_steps)

    print("E")
    res = 0
    full_square_count_center = full_square_count_min if partial_square_diagonal_count % 2 == 1 else full_square_count_max
    full_square_count_not_center = full_square_count_min if partial_square_diagonal_count % 2 == 0 else full_square_count_max
    res += len(full_square_positions_even) * \
        (full_square_count_center if steps %
         2 == 1 else full_square_count_not_center)
    res += len(full_square_positions_odd) * \
        (full_square_count_center if steps %
         2 == 0 else full_square_count_not_center)
    res += len(left_tip_positions) + len(right_tip_positions) + len(top_tip_positions) + \
        len(bottom_tip_positions)
    res += (len(bottom_left_high_diag_positions) + len(top_left_high_diag_positions) +
            len(bottom_right_high_diag_positions) + len(top_right_high_diag_positions)) * partial_square_diagonal_count
    res += (len(bottom_left_low_diag_positions) + len(top_left_low_diag_positions) +
            len(bottom_right_low_diag_positions) + len(top_right_low_diag_positions)) * (partial_square_diagonal_count - 1)
    print(res)

    print("full square even", len(full_square_positions_even), " * ",
          (full_square_count_center if steps % 2 == 1 else full_square_count_not_center))
    print("full square odd", len(full_square_positions_odd), " * ",
          (full_square_count_center if steps % 2 == 0 else full_square_count_not_center))
    print("tips", "left", len(left_tip_positions), "right", len(right_tip_positions),
          "top",  len(top_tip_positions), "bottom", len(bottom_tip_positions))
    print("(", len(bottom_left_high_diag_positions), " + ", len(top_left_high_diag_positions), " + ",
          len(bottom_right_high_diag_positions), " + ", len(top_right_high_diag_positions), ") * ", partial_square_diagonal_count)
    print("(", len(bottom_left_low_diag_positions), " + ", len(top_left_low_diag_positions), " + ",
          len(bottom_right_low_diag_positions), " + ", len(top_right_low_diag_positions), ") * (", partial_square_diagonal_count, " - 1)")
    print("diag_high_steps", diag_high_steps)
    print("diag_low_steps", diag_low_steps)
    print("tips_steps", tips_steps)
