
from minmax import Connect4MinMax
from mcts import Connect4MCTS
from connect_four import Connect4
from transposition_table import Connect4TranspositionTable
import time
import numpy as np

# Game settings
NUM_COLUMNS = 7
COLUMN_HEIGHT = 6
FOUR = 4

PLAYER_ONE = 1
PLAYER_TWO = -1

# MinMax settings
MINMAX_ITER_DEEP_MAX_DEPTH = 10
MINMAX_ITER_DEEP_TIMEOUT = 10

# MTCS settings
MTCS_MAX_ITER = 5000


class TermColors:
    YELLOW = '\x1b[7;30;43m'
    RED = '\x1b[7;30;41m'
    ENDC = '\x1b[0m'


# Game interface methods
def print_board(board):
    s = ""
    for c in range(COLUMN_HEIGHT-1, -1, -1):
        for r in range(0, NUM_COLUMNS, 1):
            if board[r, c] == PLAYER_ONE:
                s += TermColors.YELLOW + "O" + TermColors.ENDC
            elif board[r, c] == PLAYER_TWO:
                s += TermColors.RED + "O" + TermColors.ENDC
            else:
                s += "O"
            s += " "
        s += "\n"

    print(s)


def get_player_name(player):
    if player == PLAYER_ONE:
        return "P1"
    return "P2"


if __name__ == "__main__":
    c4 = Connect4(NUM_COLUMNS, COLUMN_HEIGHT, FOUR)

    tt = Connect4TranspositionTable(MINMAX_ITER_DEEP_MAX_DEPTH)
    minmax = Connect4MinMax(
        c4, tt, MINMAX_ITER_DEEP_MAX_DEPTH, MINMAX_ITER_DEEP_TIMEOUT)

    mcts = Connect4MCTS(c4, MTCS_MAX_ITER)

    board = c4.init_board()
    print_board(board)

    initial_player = PLAYER_ONE
    if np.random.uniform() > .5:
        initial_player = PLAYER_TWO

    rounds = 0
    while True:
        if len(c4.get_valid_moves(board)) == 0:
            print("MTCS and MINMAX tied!")
            break

        rounds += 1
        print("MTCS is thinking...")
        start = time.time()
        ai_move = mcts.find_best_move(board, -initial_player)
        end = time.time()
        print(
            f"{get_player_name(-initial_player)} MTCS put a disk in column {ai_move[1]} ({end - start} seconds)")
        c4.play(board, ai_move[1], -initial_player)
        print_board(board)
        if c4.four_in_a_row(board, -initial_player):
            print(f"{get_player_name(-initial_player)} MTCS won in {rounds} rounds!")
            break

        print("MINMAX is thinking...")
        start = time.time()
        #col = int(input("Enter column(0-6):"))
        ai_move = minmax.predict_best_move(board, initial_player)
        end = time.time()
        print(
            f"{get_player_name(initial_player)} MINMAX put a disk in column {ai_move[0]} ({end - start} seconds)")
        c4.play(board, ai_move[0], initial_player)
        print_board(board)
        if c4.four_in_a_row(board, initial_player):
            print(f"{get_player_name(initial_player)} MINMAX won in {rounds} rounds!")
            break

    tt.print_stats()
    minmax.print_stats()
    mcts.print_stats()
