import copy

MASS_NUM = 6


def init_board():
    mass = {
        'is_pass': False,
        'order': -1,
    }
    return [[copy.deepcopy(mass) for i in range(MASS_NUM)] for j in range(MASS_NUM)]


def get_initial_position():
    # TODO ランダムにする
    return (2, 2)


def is_finished(board, current_posiotion, initial_position):
    for row in board:
        for mass in row:
            if mass['is_pass'] is False:
                return False
    return True


def can_move_initial_position(board, initial_position):
    tmp = []
    # -1, 1, 2, -2の組み合わせ
    tmp.append((initial_position[0] + 1, initial_position[1] + 2))
    tmp.append((initial_position[0] + 1, initial_position[1] - 2))
    tmp.append((initial_position[0] - 1, initial_position[1] + 2))
    tmp.append((initial_position[0] - 1, initial_position[1] - 2))
    tmp.append((initial_position[0] + 2, initial_position[1] + 1))
    tmp.append((initial_position[0] + 2, initial_position[1] - 1))
    tmp.append((initial_position[0] - 2, initial_position[1] + 1))
    tmp.append((initial_position[0] - 2, initial_position[1] - 1))

    next_positions = []
    for np in tmp:
        # マスに収まっていない位置を削除
        if not (0 <= np[0] < MASS_NUM and 0 <= np[1] < MASS_NUM):
            continue
        if board[np[0]][np[1]]['is_pass'] is False:
            return True

    return False

def get_next_positions(board, current_position):
    tmp = []
    # -1, 1, 2, -2の組み合わせ
    tmp.append((current_position[0] + 1, current_position[1] + 2))
    tmp.append((current_position[0] + 1, current_position[1] - 2))
    tmp.append((current_position[0] - 1, current_position[1] + 2))
    tmp.append((current_position[0] - 1, current_position[1] - 2))
    tmp.append((current_position[0] + 2, current_position[1] + 1))
    tmp.append((current_position[0] + 2, current_position[1] - 1))
    tmp.append((current_position[0] - 2, current_position[1] + 1))
    tmp.append((current_position[0] - 2, current_position[1] - 1))

    next_positions = []
    for np in tmp:
        # マスに収まっていない位置を削除
        if not (0 <= np[0] < MASS_NUM and 0 <= np[1] < MASS_NUM):
            continue
        # すでに通ったマスを削除
        if board[np[0]][np[1]]['is_pass'] is True:
            continue

        next_positions.append(np)

    # print(str(board[current_position[0]][current_position[1]]['order']) + ': ' + str(current_position) + ' -> ' + str(next_positions))
    return next_positions


def solve(board, current_position, initial_position):
    if not can_move_initial_position(board, initial_position):
        return None

    if is_finished(board, current_position, initial_position):
        return board

    # print('---- board ----')
    # print_board(board)

    next_positions = get_next_positions(board, current_position)
    if not next_positions:
        return None

    sorted_next_positions = []
    for np in next_positions:
        sorted_next_positions.append((len(get_next_positions(board, np)), np))

    sorted_next_positions = [np[1] for np in sorted(sorted_next_positions, key=lambda x: x[0])]

    for next_position in sorted_next_positions:
        next_order = board[current_position[0]][current_position[1]]['order'] + 1
        next_board = copy.deepcopy(board)
        next_board[next_position[0]][next_position[1]]['is_pass'] = True
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
    board[initial_position[0]][initial_position[1]]['is_pass'] = True
    board[initial_position[0]][initial_position[1]]['order'] = 1

    print('----- initial board -----')
    print_board(board)

    solved_board = solve(board, initial_position, initial_position)

    print('----- solved board -----')
    print_board(solved_board)

if __name__ == "__main__":
    main()