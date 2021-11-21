import numpy as np


class Connect4:
    def __init__(self, num_columns, column_height, four):
        self.num_columns = num_columns
        self.column_height = column_height
        self.four = four

    def init_board(self):
        return np.zeros((self.num_columns, self.column_height))

    def get_valid_moves(self, board):
        """Returns columns where a disc may be played"""
        return [n for n in range(self.num_columns) if board[n, self.column_height - 1] == 0]

    def play(self, board, column, player):
        """Updates `board` as `player` drops a disc in `column`"""
        (index,) = next(
            (i for i, v in np.ndenumerate(board[column]) if v == 0))
        board[column, index] = player

    def take_back(self, board, column):
        """Updates `board` removing top disc from `column`"""
        (index,) = [i for i, v in np.ndenumerate(board[column]) if v != 0][-1]
        board[column, index] = 0

    def four_in_a_row(self, board, player):
        """Checks if `player` has a 4-piece line"""
        return (
            any(
                all(board[c, r] == player)
                for c in range(self.num_columns)
                for r in (list(range(n, n + self.four)) for n in range(self.column_height - self.four + 1))
            )
            or any(
                all(board[c, r] == player)
                for r in range(self.column_height)
                for c in (list(range(n, n + self.four)) for n in range(self.num_columns - self.four + 1))
            )
            or any(
                np.all(board[diag] == player)
                for diag in (
                    (range(ro, ro + self.four), range(co, co + self.four))
                    for ro in range(0, self.num_columns - self.four + 1)
                    for co in range(0, self.column_height - self.four + 1)
                )
            )
            or any(
                np.all(board[diag] == player)
                for diag in (
                    (range(ro, ro + self.four), range(co + self.four - 1, co - 1, -1))
                    for ro in range(0, self.num_columns - self.four + 1)
                    for co in range(0, self.column_height - self.four + 1)
                )
            )
        )

    def eval_terminal(self, board, player):
        if self.four_in_a_row(board, player):
            return 10000000
        elif self.four_in_a_row(board, -player):
            return -10000000
        else:
            return 0

    def calc_slot_score(self, slot, player):
        v = player * sum(slot)

        # Slot with 2 player disks and 2 free places
        if v == 2 and np.count_nonzero(slot) == 2:
            return 32
        # Slot with 3 player disks and 1 free place
        elif v == 3:
            return 64
        # Slot with 4 player disks
        elif v == 4:
            return 512
        # Slot with 3 opponent disks and 1 free place
        elif v == -3:
            return -128
        return 0

    def calc_board_score(self, board, player):
        score = 0

        # add positive score to central moves
        central_col = float(self.num_columns) / 2
        central_slots = board[int(central_col), :]
        if(central_col.is_integer()):
            central_slots = np.append(
                central_slots, board[int(central_col)-1, :])
        central_disks = len(central_slots[central_slots == player])
        score += central_disks * 16

        cols_four_slots = [board[c, r] for c in range(self.num_columns)
                           for r in (list(range(x, x + self.four)) for x in range(self.column_height - self.four + 1))]
        for slot in cols_four_slots:
            score += self.calc_slot_score(slot, player)

        rows_four_slots = [board[c, r]
                           for r in range(self.column_height)
                           for c in (list(range(x, x + self.four)) for x in range(self.num_columns - self.four + 1))]
        for slot in rows_four_slots:
            score += self.calc_slot_score(slot, player)

        pos_diag_four_slots = [board[diag] for diag in (
            (range(ro, ro + self.four), range(co, co + self.four))
            for ro in range(0, self.num_columns - self.four + 1)
            for co in range(0, self.column_height - self.four + 1))]
        for slot in pos_diag_four_slots:
            score += self.calc_slot_score(slot, player)

        neg_diag_four_slots = [board[diag] for diag in (
            (range(ro, ro + self.four), range(co + self.four - 1, co - 1, -1))
            for ro in range(0, self.num_columns - self.four + 1)
            for co in range(0, self.column_height - self.four + 1))]
        for slot in neg_diag_four_slots:
            score += self.calc_slot_score(slot, player)

        return score

    def get_ordered_valid_moves(self, board, player):
        valid_moves = self.get_valid_moves(board)

        moves = []
        for move in valid_moves:
            self.play(board, move, player)
            score = self.calc_board_score(board, player)
            moves.append((move, score))
            self.take_back(board, move)

        moves.sort(key=lambda k: k[1], reverse=True)
        return moves
