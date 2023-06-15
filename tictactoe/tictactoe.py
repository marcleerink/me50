from copy import deepcopy

"""
Tic Tac Toe Player
"""


X = "X"
O = "O"
EMPTY = None


class InvalidActionError(Exception):
    pass


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = 0
    o_count = 0
    for row in board:
        x_count += row.count(X)
        o_count += row.count(O)

    if x_count <= o_count:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    actions = set()
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == EMPTY:
                actions.add((i, j))

    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if board[action[0]][action[1]] != EMPTY:
        raise InvalidActionError("Invalid action")
    new_board = deepcopy(board)
    new_board[action[0]][action[1]] = player(board)
    return new_board


def check_win(row):
    x_count = row.count(X)
    o_count = row.count(O)
    if x_count == 3:
        return X
    elif o_count == 3:
        return O
    else:
        return None


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(len(board)):
        # check rows
        row = board[i]
        result = check_win(row)
        if result:
            return result

        # check columns
        column = [board[j][i] for j in range(len(board))]
        result = check_win(column)
        if result:
            return result

    # check diagonals
    diagonal1 = [board[i][i] for i in range(len(board))]
    result = check_win(diagonal1)
    if result:
        return result

    diagonal2 = [board[i][len(board) - 1 - i] for i in range(len(board))]
    result = check_win(diagonal2)
    if result:
        return result

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) or not actions(board):
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    result = winner(board)
    if result == X:
        return 1
    elif result == O:
        return -1
    else:
        return 0


def max_value(board):
    if terminal(board):
        return utility(board)

    v = -2
    for action in actions(board):
        v = max(v, min_value(result(board, action)))

    return v


def min_value(board):
    if terminal(board):
        return utility(board)

    v = 2
    for action in actions(board):
        v = min(v, max_value(result(board, action)))

    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if terminal(board):
        return None

    if player(board) == X:
        best_score = -2
        best_move = None
        for action in actions(board):
            score = min_value(result(board, action))
            if score > best_score:
                best_score = score
                best_move = action

    else:
        best_score = 2
        best_move = None
        for action in actions(board):
            score = max_value(result(board, action))
            if score < best_score:
                best_score = score
                best_move = action

    return best_move
