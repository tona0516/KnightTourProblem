import sys
import copy
import argparse

BOARD_LENGTH = 8

is_solve_closed = False

def init_board():
    """initialize board

    Returns:
        list -- 2d array of square
    """
    return [[0 for i in range(BOARD_LENGTH)] for j in range(BOARD_LENGTH)]


def get_arguments():
    """get inputs from command line argument

    Returns:
        list -- arguments
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('row', type=int, help='initial row position', choices=range(0, 8))
    parser.add_argument('column', type=int, help='initial column position', choices=range(0, 8))
    parser.add_argument('-c', '--closed', help="solve closed knight's tour problem", action='store_true')

    return parser.parse_args()


def is_solved(board, current_posiotion, initial_position):
    """check to have solved

    Arguments:
        board {list} -- board
        current_posiotion {tuple} -- current knight's position
        initial_position {tuple} -- initial knight's position

    Returns:
        bool -- True if this problem has solved
    """
    global is_solve_closed

    if is_solve_closed is True:
        # knight can move from current position to initial one?
        next_positions = get_next_positions(board, current_posiotion, enable_passed_check=False)
        if not (initial_position in next_positions):
            return False

    # all squares are passed?
    for row in board:
        for square in row:
            if square == 0:
                return False

    return True


def get_next_positions(board, current_position, enable_passed_check=True):
    """get positions where knight can move from its current position

    Arguments:
        board {list} -- board
        current_position {tuple} -- current knight's position
        enable_passed_check {bool} -- exclude passed positions if it is True
    Returns:
        list -- positions
    """
    # calculate
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

    # exclude passed positions
    not_passed_next_positions = [np for np in next_positions if board[np[0]][np[1]] == 0]
    return not_passed_next_positions


def sort_by_warnsdorfs_rule(board, next_positions):
    """sort by Warnsdorf's rule

    Arguments:
        board {list} -- board
        next_positions {list} -- positions

    Returns:
        list -- sorted positions
    """
    tmp = [(len(get_next_positions(board, np)), np) for np in next_positions]
    return [np[1] for np in sorted(tmp, key=lambda x: x[0])]


def solve(board, current_position, initial_position):
    """solve the problem by depth-first search

    Arguments:
        board {list} -- board
        current_position {tuple} -- current knight's position
        initial_position {tuple} -- initial knight's position

    Returns:
        list -- board
    """
    if is_solved(board, current_position, initial_position):
        return board

    next_positions = get_next_positions(board, current_position)
    if not next_positions:
        return None

    sorted_next_positions = sort_by_warnsdorfs_rule(board, next_positions)

    # go next step
    for next_position in sorted_next_positions:
        next_order = board[current_position[0]][current_position[1]] + 1
        next_board = copy.deepcopy(board)
        next_board[next_position[0]][next_position[1]] = next_order
        ret = solve(next_board, next_position, initial_position)
        if ret is not None:
            return ret

    return None


def print_board(board):
    """output board

    Arguments:
        board {list} -- board
    """
    for row in board:
        for square in row:
            print("{0:2d}".format(square), end=' ')
        print()


def main():
    global is_solve_closed

    args = get_arguments()
    is_solve_closed = args.closed
    initial_position = (args.row, args.column)

    board = init_board()
    board[initial_position[0]][initial_position[1]] = 1

    print('----- initial board -----')
    print_board(board)
    print()

    solved_board = solve(board, initial_position, initial_position)

    if solved_board is None:
        print('not found the solution...')
        sys.exit(1)

    print('----- solved board -----')
    print_board(solved_board)

if __name__ == "__main__":
    main()
