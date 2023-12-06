# Tic-Tac-Toe

I've written a Tic-Tac-Toe AI that uses the Minimax algorithm, which is a backtracking search algorithm, to find the optimal move for a player, assuming that the opponent also plays optimally.

## Reflection

There are several ways to improve the code that i've written and reduce the number of states visited.

### Alpha-Beta Pruning

The minimax algorithm can be optimized by making use of alpha-beta pruning. This reduces the number of nodes evaluated in the search tree by pruning branches that cannot possibly influence the final decision. This can be implemented with two variables, 'alpha' and 'beta, which represent the minimum score that the maximizing player is assuered of ('alpha') and the maximum score that the minimizing player is assured of ('beta'). I've implemented this in the last version.

#### This is how it works in my code:

##### Minimax function

The minimax function decides the best move.
It calls max_value if it's X's turn or min_value if it's O's turn.
These functions recursively call each other and themselves, evaluating the board until terminal states are reached.
Alpha-beta pruning is used here to cut off unnecessary evaluations.

##### In the max_value function:

- The function is trying to find the maximum score the maximizer can achieve.
- It initializes v to -2 to find a value better than this.
- For each possible action, it calls min_value (which considers the opponent's minimizing strategy).
- If the value returned by min_value is greater than the current v, then v is updated to this new value.
- The alpha value is then updated to be the maximum of the current alpha or the new v.
- If at any point beta becomes less than or equal to alpha, the function breaks out of the loop because all further exploration is useless (this is the pruning part). The algorithm has found a move that guarantees the maximizer a value greater than or equal to alpha, and since the minimizer would never allow that (as the minimizer is trying to minimize the value), the remaining subtrees don't need to be evaluated.

##### In the min_value function

- The function is trying to find the minimum score the minimizer can achieve.
- It initializes v to +2 to find a value worse than this (from the perspective of the maximizer).
- For each possible action, it calls max_value (which considers the maximizer's maximizing strategy).
- If the value returned by max_value is less than the current v, then v is updated to this new value.
- The beta value is then updated to be the minimum of the current beta or the new v.
- If at any point beta becomes less than or equal to alpha, the function breaks out of the loop. This means that the minimizer has found a move that guarantees a value less than or equal to beta, and since the maximizer would never allow that (as the maximizer is trying to maximize the value), the remaining subtrees are pruned.

### Depth First Search

The minimax algorithm implemented uses Depth First Search. The max_value and min_value functions call each other recusively, going deeper into the tree until they reach a terminal state. Once finished with one branch, they then backtrack to explore a different branch of the game.
