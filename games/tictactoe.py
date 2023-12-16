import numpy as np
import minimax

PLAYER_PIECE = 1
COMP_PIECE = 2

"""
Board is classicly build like this:
    [
        [0,2,0],
        [1,0,1],
        [1,2,2]
    ] as a numpy matrix (3x3)
    Where
        0 is a free space
        1 is PLAYER_PIECE
        2 is COMP_PIECE
"""

def generateMoves():
    """generates all moves that could be made, even the ones that are not possible

    Yields:
        int: the move
    """    
    for i in range(9):
        yield i

def areMovesLeft(board: np.ndarray) -> bool:
    """determines if there is a move left to be played

    Args:
        board (np.ndarray): the current game state

    Returns:
        bool: if there is a possible move left
    """    
    return np.any(board == 0)

def checkWinner(board: np.ndarray) -> int:
    """checks if there is a winner and returns him

    Args:
        board (np.ndarray): the current game state

    Returns:
        int: the winner
    """    
    for i in range(3):
        #Check Rows
        if np.all(board[i] == board[i][0]):
            return board[i][0]
        #Check Columns
        if np.all(board[:,i] == board[:,i][0]):
            return board[:,i][0]
    
    #Check diagonals
    if np.all(board.diagonal() == board.diagonal()[0]):
        return board.diagonal()[0]
    if np.all(np.flipud(board).diagonal() == np.flipud(board).diagonal()[0]):
        return np.flipud(board).diagonal()[0]
    
    #No winner
    return 0

def playPiece(board: np.ndarray, piece: int, field: int) -> tuple[bool, tuple[int, int]]:
    """places a piece on the board if possible

    Args:
        board (np.ndarray): the current game state
        piece (int): the piece needed to be placed
        field (int): the field the where the piece is placed

    Returns:
        (bool, (int,int)): true if the piece is placed or not and the coordinates where it was places
    """
    y = field // 3
    x = field % 3
    
    if board[y,x]: return False, (-1, -1)
    
    board[y,x] = piece
    return True, (y,x)

def evaluateBoard(board: np.ndarray) -> int:
    """returns a score for the given board

    Args:
        board (np.ndarray): the current game state

    Returns:
        int: the score of the board
    """
    winner = checkWinner(board)
    if winner == PLAYER_PIECE: return -1
    elif winner == COMP_PIECE: return 1
    else: return 0

def findBestMove(board: np.ndarray) -> int:
    """returns the current best move

    Args:
        board (np.ndarray): the current game state

    Returns:
        int: the move that needs to be played
    """
    copiedBoard = np.copy(board)
    return minimax.minimaxAlgo(copiedBoard, PLAYER_PIECE, COMP_PIECE,
                                evaluateBoard, playPiece, areMovesLeft, checkWinner, generateMoves)

if __name__ == "__main__":
    board = np.array([
                [0,0,0],
                [0,0,0],
                [0,0,0]
            ])
    
    current_PLAYER_PIECE = PLAYER_PIECE
    print(board)
    while areMovesLeft(board) and not checkWinner(board):
        if current_PLAYER_PIECE == PLAYER_PIECE:
            target_field = int(input("field: "))
            while(not playPiece(board, PLAYER_PIECE, target_field)[0]):
                target_field = int(input("NEU field: "))
        else:
            move = findBestMove(board)
            playPiece(board, COMP_PIECE, move)
            
        print(board)
            
        if current_PLAYER_PIECE == PLAYER_PIECE: current_PLAYER_PIECE = COMP_PIECE
        else: current_PLAYER_PIECE = PLAYER_PIECE
        
    if not checkWinner(board):
        print("Unentschieden")
    else: print(checkWinner(board))