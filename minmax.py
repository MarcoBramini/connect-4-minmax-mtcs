import time
import numpy as np


class Connect4MinMax:
    def __init__(self, c4, tt, iter_deep_max_depth, iter_deep_timeout_seconds):
        self.c4 = c4
        self.tt = tt
        self.iter_deep_max_depth = iter_deep_max_depth
        self.iter_deep_timeout_seconds = iter_deep_timeout_seconds
        self.analyzed_moves_count = 0
        self.skipped_moves_cache = 0

    def predict_best_move(self, board, player_to_maximize):
        best_move = None
        start = time.time()

        for depth in range(1, self.iter_deep_max_depth+1):
            end = time.time()
            if end-start > self.iter_deep_timeout_seconds:
                break
            print("Try depth:", depth)
            best_move = self.minmax(board, player_to_maximize, depth)
            print("Found move:", best_move)
            self.tt.print_stats()
            self.print_stats()

        return best_move

    def minmax(self, board, player, depth, alpha=-np.Infinity, beta=np.Infinity):
        self.analyzed_moves_count += 1
        alpha_orig = alpha
        # Try searching for a cached score for the current board
        # or at least boundaries to narrow the research.
        # Cached valued is in the form: (score, flag)
        cached_move = self.tt.get(board, player, depth)
        if cached_move != None:
            cached_score, flag = cached_move
            if flag == "EXACT":
                self.skipped_moves_cache += 1
                return (None, cached_score)
            elif flag == "LBOUND":
                alpha = max(alpha, cached_score)
            elif flag == "UBOUND":
                beta = min(beta, cached_score)

            if alpha >= beta:
                self.skipped_moves_cache += 1
                return (None, cached_score)

        valid_moves = self.c4.get_ordered_valid_moves(board, player)
        terminal_value = self.c4.eval_terminal(board, player)
        if len(valid_moves) == 0 or terminal_value != 0:
            return (None, terminal_value)

        if depth == 0:
            return (None, self.c4.calc_board_score(board, player))

        best_move = (np.random.choice(
            [m for m, _ in valid_moves]), -np.Infinity)
        for move, _ in valid_moves:
            self.c4.play(board, move, player)

            next_move_score = -self.minmax(
                board, -player, depth - 1, -beta, -alpha)[1]

            next_move = (move, next_move_score)
            best_move = max([best_move, next_move], key=lambda k: k[1])

            self.c4.take_back(board, move)

            alpha = max(alpha, best_move[1])

            if alpha >= beta:
                break

        # Cache the score found for the current move
        flag = "EXACT"
        if best_move[1] <= alpha_orig:
            flag = "UBOUND"
        elif best_move[1] >= beta:
            flag = "LBOUND"
        self.tt.put(board, player, depth, best_move[1], flag)

        return best_move

    def print_stats(self):
        print(
            f"Minmax: analyzed moves: {self.analyzed_moves_count} recovered cached moves:{self.skipped_moves_cache}")
