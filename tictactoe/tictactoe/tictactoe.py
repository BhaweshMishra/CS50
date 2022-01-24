"""
Tic Tac Toe Player
"""

from asyncio.windows_events import INFINITE
import copy
import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x = 0
    o = 0
    for i in board:
        x += i.count(X)
        o += i.count(O)
    
    if x > o:
        return O
    
    if x == o:
        return X

    else:
        return X   

    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = []
    for i in range(3):
        
        for j in range(3):
            
            if board[i][j] == EMPTY:
                possible_actions.append((i,j))
    return possible_actions

    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    deepboard = copy.deepcopy(board)
    deepboard[action[0]][action[1]] = player(board)
    return deepboard

    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    winning_combinations = [
                            [(0,0),(0,1),(0,2)],
                            [(1,0),(1,1),(1,2)],
                            [(2,0),(2,1),(2,2)],
                            [(0,0),(1,0),(2,0)],
                            [(0,1),(1,1),(2,1)],
                            [(0,2),(1,2),(2,2)],
                            [(0,0),(1,1),(2,2)],
                            [(0,2),(1,1),(2,0)],
    ]

    for i in winning_combinations:
        if board[i[0][0]][i[0][1]] == X and board[i[1][0]][i[1][1]] == X and board[i[2][0]][i[2][1]] == X:
            return X
        if board[i[0][0]][i[0][1]] == O and board[i[1][0]][i[1][1]] == O and board[i[2][0]][i[2][1]] == O:  
            return O           
    
    return None

    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    
    if winner(board) == X or winner(board) == O:
        return True
    for i in board:
        for j in i:
            if j is EMPTY:
                return False
    return True
    
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    if winner(board) == X:
        return 1
    if winner(board) == O:
        return -1
    return 0

    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    possible_outcomes = []
    possible_actions = actions(board)
    
    if player(board) == X:
        for action in possible_actions:
            possible_outcomes.append(minval(result(board, action)))
        max_index = possible_outcomes.index(max(possible_outcomes))
        return possible_actions[max_index]
    
    if player(board) == O:
        for action in possible_actions:
            possible_outcomes.append(maxval(result(board, action)))
        min_index = possible_outcomes.index(min(possible_outcomes))
        return possible_actions[min_index]
        


    raise NotImplementedError

def maxval(board):
    '''
    v = -∞
    if Terminal(state):
        return Utility(state)
    for action in Actions(state):
        v = Max(v, Min-Value(Result(state, action)))
    return v
    '''

    val = -INFINITE
    if terminal(board) is True:
        return utility(board)
    for action in actions(board):
        val = max(val, minval(result(board, action)))
    return val

def minval(board):
    '''
    v = ∞
    if Terminal(state):
        return Utility(state)
    for action in Actions(state):
        v = Min(v, Max-Value(Result(state, action)))
    return v
    '''

    val = INFINITE
    if terminal(board):
        return utility(board)
    for action in actions(board):
        val = min(val, maxval(result(board, action)))
    return val