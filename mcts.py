import numpy as np


class Connect4MCNode:
    def __init__(self, c4, board, player, move=None, parent=None):
        self.c4 = c4
        self.board = board
        self.move = move
        self.player = player
        self.parent = parent
        self.wins = 0
        self.visits = 1
        self.children = []
        self.available_moves = c4.get_valid_moves(board)

    def add_child(self, move):
        child_board = np.copy(self.board)
        child = Connect4MCNode(self.c4, child_board, -self.player, move, self)
        self.children.append(child)
        self.c4.play(child.board, move, -self.player)
        child.available_moves = self.c4.get_valid_moves(child.board)
        self.available_moves.remove(move)
        return child

    def update(self, simulation_result):
        self.visits += 1
        self.wins += simulation_result

    def __str__(self):
        return f"{self.move} | {self.wins} | {self.visits} | {[f'{child.move} | {child.wins} | {child.visits} | {child.wins/child.visits}' for child in self.children]}"

    def select_child_uct(self):
        max_score, max_child = -np.Infinity, None
        for child in self.children:
            if (child.visits == 0):
                continue
            score = child.wins / child.visits + \
                np.sqrt(2*np.log(self.visits) / child.visits)
            if score > max_score:
                max_child = child
                max_score = score
        return max_child


class Connect4MCTS:
    def __init__(self, c4, max_iter, expansion_rate, exploitation_rate):
        self.max_iter = max_iter
        self.expansion_rate = expansion_rate  # maybe 0.5
        self.exploitation_rate = exploitation_rate  # maybe 0.5
        self.c4 = c4

    def select_node(self, node):
        def random_depth(node, stop_prob):
            current_node = node
            while np.random.uniform() < stop_prob:
                if len(current_node.children) == 0:
                    return current_node
                current_node = np.random.choice(current_node.children)
            return current_node

        r = np.random.uniform()
        # If random value above expansion_rate, select low depths
        if r > self.expansion_rate:
            return random_depth(node, 0.4)
        # Else select high depths
        else:
            return random_depth(node, 0.8)

    def select_node2(self, node):
        while len(node.children) != 0:
            node = node.select_child_uct()
        return node

    def expand_node(self, node):
        while len(node.available_moves) != 0:
            move = np.random.choice(node.available_moves)
            node.add_child(move)

    def simulate(self, node):
        board_copy = np.copy(node.board)
        player = node.player
        if self.c4.four_in_a_row(board_copy, player):
            return player
        if self.c4.four_in_a_row(board_copy, -player):
            return -player

        while len(moves := self.c4.get_valid_moves(board_copy)) != 0:
            player = -player
            c = np.random.choice(moves)
            self.c4.play(board_copy, c, player)
            if self.c4.four_in_a_row(board_copy, player):
                return player

        return 0

    def backpropagate(self, node, sim_res):
        while node is not None:
            node.update(sim_res * node.player)
            node = node.parent

    def find_best_move(self, board, player):
        root = Connect4MCNode(self.c4, board, -player)
        iterations = 0
        while iterations < self.max_iter:
            # Selection
            # Select a node for expansion
            selected_node = self.select_node2(root)

            # Expansion
            # Expand the selected node
            self.expand_node(selected_node)

            # Simulation
            sim_res = self.simulate(selected_node)

            # Update
            self.backpropagate(selected_node, sim_res)
            iterations += 1

        print(root)
        return root, sorted(root.children, key=lambda child: child.wins/child.visits)[-1].move
