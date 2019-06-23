import copy

MASS_NUM = 8


def init_board():
    mass = {
        'is_passed': False,
        'order': 0,
    }
    return [[copy.deepcopy(mass) for i in range(MASS_NUM)] for j in range(MASS_NUM)]


def get_initial_position():
    return (0, 0)


def is_finished(board, current_posiotion, initial_position):
    # 現在位置から初期位置に戻れること
    next_positions = get_next_positions(board, current_posiotion)
    if not (initial_position in next_positions):
        return False

    # すべて通過していること
    for row in board:
        for mass in row:
            if mass['is_passed'] is False:
                return False

    return True


def get_next_positions(board, current_position):
    diffs = [
        (1, 2),
        (1, -2),
        (-1, 2),
        (-1, -2),
        (2, 1),
        (2, -1),
        (-2, 1),
        (-2, -1),
    ]
    tmp = [(current_position[0] + diff[0], current_position[1] + diff[1]) for diff in diffs]
    next_positions = [np for np in tmp if 0 <= np[0] < MASS_NUM and 0 <= np[1] < MASS_NUM]
    return next_positions


def get_jumpable_positions(board, current_position):
    next_positions = get_next_positions(board, current_position)
    jumpable_positions = [np for np in next_positions if board[np[0]][np[1]]['is_passed'] is False]
    return jumpable_positions


def solve(board, current_position, initial_position):
    if is_finished(board, current_position, initial_position):
        return board

    next_positions = get_jumpable_positions(board, current_position)
    if not next_positions:
        return None

    sorted_next_positions = []
    for np in next_positions:
        sorted_next_positions.append((len(get_jumpable_positions(board, np)), np))

    sorted_next_positions = [np[1] for np in sorted(sorted_next_positions, key=lambda x: x[0])]

    for next_position in sorted_next_positions:
        next_order = board[current_position[0]][current_position[1]]['order'] + 1
        next_board = copy.deepcopy(board)
        next_board[next_position[0]][next_position[1]]['is_passed'] = True
        next_board[next_position[0]][next_position[1]]['order'] = next_order
        ret = solve(next_board, next_position, initial_position)
        if ret is not None:
            return ret

    return None


def print_board(board):
    for row in board:
        for mass in row:
            print("{0:2d}".format(mass['order']), end=' ')
        print()


def main():
    board = init_board()
    initial_position = get_initial_position()
    board[initial_position[0]][initial_position[1]]['is_passed'] = True
    board[initial_position[0]][initial_position[1]]['order'] = 1

    print('----- initial board -----')
    print_board(board)

    solved_board = solve(board, initial_position, initial_position)

    print('----- solved board -----')
    print_board(solved_board)

if __name__ == "__main__":
    main()
