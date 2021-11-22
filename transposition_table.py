import numpy as np


class Connect4TranspositionTable:
    def __init__(self, max_depth):
        self.tt = {}  # This should be LRU :( )
        self.max_depth = max_depth
        self.total_hits = 0

    def _hash_state(self, board, player, depth):
        return hash((board.tobytes(), str(player), str(depth)))

    def put(self, board, player, depth, score, flag):
        # Only cached values with lower depth of the current level must be used
        # Cache the current value with all the depths between max_depth and the current depth
        for d in range(0, depth+1):
            self.tt[self._hash_state(board, player, d)] = (score, flag)
            # Also cache the identical board mirrored on the y axis
            self.tt[self._hash_state(np.flip(board, axis=0), player, d)] = (
                score, flag)

    def get(self, board, player, depth):
        v = self.tt.get(self._hash_state(board, player, depth))
        if v != None:
            self.total_hits += 1
        return v

    def print_stats(self):
        print(f"Cache: hits:{self.total_hits} size:{len(self.tt)}")
