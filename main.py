
from minmax import Connect4MinMax
from connect_four import Connect4
from transposition_table import Connect4TranspositionTable
import time
import numpy as np

NUM_COLUMNS = 7
COLUMN_HEIGHT = 6
FOUR = 4

PLAYER_ONE = 1
PLAYER_TWO = -1


class TermColors:
    YELLOW = '\x1b[7;30;43m'
    RED = '\x1b[7;30;41m'
    ENDC = '\x1b[0m'


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


# 34333
if __name__ == "__main__":
    max_depth = 8

    tt = Connect4TranspositionTable(max_depth)
    c4 = Connect4(NUM_COLUMNS, COLUMN_HEIGHT, FOUR)
    minmax = Connect4MinMax(c4, tt, max_depth, 10)

    board = c4.init_board()
    print_board(board)

    initial_player = PLAYER_ONE
    if np.random.uniform() > .5:
        initial_player = PLAYER_TWO
    while True:

        start = time.time()
        print(c4.get_valid_moves(board))
        #col = int(input("Enter column(0-6):"))
        ai_move = minmax.predict_best_move(board, initial_player)
        end = time.time()
        print(get_player_name(initial_player), ai_move, end - start, "s")
        c4.play(board, ai_move[0], initial_player)
        print_board(board)
        if c4.four_in_a_row(board, initial_player):
            print(get_player_name(initial_player) + " won")
            break

        start = time.time()
        ai_move = minmax.predict_best_move(board, -initial_player)
        end = time.time()
        print(get_player_name(-initial_player), ai_move, end - start, "s")
        c4.play(board, ai_move[0], -initial_player)
        print_board(board)
        if c4.four_in_a_row(board, -initial_player):
            print(get_player_name(-initial_player) + " won")
            break

    tt.print_stats()
    minmax.print_stats()
