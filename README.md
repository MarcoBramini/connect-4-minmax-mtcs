# Connect Four

@author: Marco Bramini (s285913)  
(based on the template provided by Prof. Giovanni Squillero)

This repository contains an implementation of **MinMax** and **Monte Carlo Tree Search** solvers for Connect 4.

The main method contains an example match between the two algorithms.
They are configured to run the best match possible in a limited amount of time (from testing, each move can take maximum 50 seconds).
A faster match can be obtained setting MTCS_MAX_ITER to 500 (or 1000).

From the profiling, the most of the time spent is caused by the win checks, which could be better optimized (maybe a cache of all possible winning boards might help?).

## MinMax

The algorithm implemented is **Negamax**, a variant of MinMax.

The following features have been implemented:

- **Alpha-Beta Pruning**
- **Transposition Table** (for now is only an hashed dict, an LRU dict could be an improvement)
- **Iterative Deepening** (MINMAX_ITER_DEEP_MAX_DEPTH and MINMAX_ITER_DEEP_TIMEOUT constants can be used to configure it)

## Monte Carlo Tree Search

The algorithm is a standard **MCTS**.

The number of iterations for each search can be set using the constant MTCS_MAX_ITER.

It executes the following steps:

- **Selection**: Selects the next leaf node, that has never been processed, to be considered. The nodes are selected using the **UCT** (Upper Confidence bound for Trees) algorithm (which tries to solve the exploration vs exploitation tradeoff problem).
- **Expansion**: The selected node is expanded and its children states of the game are generated.
- **Simulation**: All the possible moves are played to reach a terminal state for the selected node.
- **Backpropagation**: The collected information about the terminal states are propagated to parent nodes.
