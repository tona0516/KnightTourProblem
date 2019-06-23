import copy

BOARD_LENGTH = 8


def init_board():
    """ボードの初期化

    Returns:
        list -- マスの2次元配列
    """
    return [[0 for i in range(BOARD_LENGTH)] for j in range(BOARD_LENGTH)]


def get_initial_position():
    """初期座標を返却

    Returns:
        tuple -- 座標
    """
    return (0, 0)


def is_finished(board, current_posiotion, initial_position):
    """終了判定

    Arguments:
        board {list} -- ボード
        current_posiotion {tuple} -- 現在座標
        initial_position {tuple} -- 初期座標

    Returns:
        bool -- 解が見つかったらTrue
    """
    # 現在座標から初期座標に戻れること
    next_positions = get_next_positions(board, current_posiotion, enable_passed_check=False)
    if not (initial_position in next_positions):
        return False

    # すべて通過していること
    for row in board:
        for square in row:
            if square == 0:
                return False

    return True


def get_next_positions(board, current_position, enable_passed_check=True):
    """現在座標から移動可能な座標を返却

    Arguments:
        board {list} -- ボード
        current_position {tuple} -- 現在座標
        enable_passed_check {bool} -- Trueなら通過した座標を除外
    Returns:
        list -- 座標のリスト
    """
    # 移動可能な座標を算出
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
    next_positions = [np for np in tmp if 0 <= np[0] < BOARD_LENGTH and 0 <= np[1] < BOARD_LENGTH]

    if enable_passed_check is False:
        return next_positions

    # すでに通過したマスを除外
    not_passed_next_positions = [np for np in next_positions if board[np[0]][np[1]] == 0]
    return not_passed_next_positions


def sort_by_Warnsdorfs_rule(board, next_positions):
    """Warnsdorf's ruleに則ってソートする

    Arguments:
        board {list} -- ボード
        next_positions {list} -- 次に移動する座標のリスト

    Returns:
        list -- ソートした次に移動する座標のリスト
    """
    tmp = [(len(get_next_positions(board, np)), np) for np in next_positions]
    return [np[1] for np in sorted(tmp, key=lambda x: x[0])]


def solve(board, current_position, initial_position):
    """再帰的に探索

    Arguments:
        board {list} -- ボード
        current_position {tuple} -- 現在座標
        initial_position {tuple} -- 初期座標

    Returns:
        list -- ボード
    """
    # 解が見つかったら終了
    if is_finished(board, current_position, initial_position):
        return board

    # 移動可能な座標を列挙
    # なければ一手戻る
    next_positions = get_next_positions(board, current_position)
    if not next_positions:
        return None

    # ソート
    sorted_next_positions = sort_by_Warnsdorfs_rule(board, next_positions)

    # 移動して次手へ
    for next_position in sorted_next_positions:
        next_order = board[current_position[0]][current_position[1]] + 1
        next_board = copy.deepcopy(board)
        next_board[next_position[0]][next_position[1]] = next_order
        ret = solve(next_board, next_position, initial_position)
        if ret is not None:
            return ret

    return None


def print_board(board):
    """ボードを標準出力

    Arguments:
        board {list} -- ボード
    """
    for row in board:
        for square in row:
            print("{0:2d}".format(square), end=' ')
        print()


def main():
    board = init_board()
    initial_position = get_initial_position()
    board[initial_position[0]][initial_position[1]] = 1

    print('----- initial board -----')
    print_board(board)

    solved_board = solve(board, initial_position, initial_position)

    print('----- solved board -----')
    print_board(solved_board)

if __name__ == "__main__":
    main()
