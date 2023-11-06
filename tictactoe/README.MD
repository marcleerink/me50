# Tic-Tac-Toe

I've written a Tic-Tac-Toe AI that uses the Minimax algorithm, which is a backtracking search algorithm, to find the optimal move for a player, assuming that the opponent also plays optimally.

## Reflection

There are several ways to improve the code that i've written and reduce the number of states visited.

### Alpha-Beta Pruning

The minimax algorithm can be optimized by making use of alpha-beta pruning. This reduces the number of nodes evaluated in the search tree by pruning brnaches that cannot possibly influence the final decision. This can be implemented with two variables, 'alpha' and 'beta, which represent the minimum score that the maximizing player is assuered of ('alpha') and the maximum score that the minimizing player is assured of ('beta').
