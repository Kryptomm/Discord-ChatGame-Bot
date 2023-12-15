import numpy as np
import minimax


PLAYER_PIECE = 1
COMP_PIECE = 2

"""
Board is classicly build like this:
    [
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,2,0,0,2,0],
        [0,1,2,1,0,1,0],
        [1,1,2,2,1,2,1],
    ] as a numpy matrix (7x6)
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
    for i in range(7):
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
    for row in range(6):
        row_str = ''.join(map(str, board[row]))
        if str(PLAYER_PIECE)*4 in row_str: return PLAYER_PIECE
        elif str(COMP_PIECE)*4 in row_str: return COMP_PIECE

    for column in range(6):
        column_str = ''.join(map(str, board[:,column]))
        if str(PLAYER_PIECE)*4 in column_str: return PLAYER_PIECE
        elif str(COMP_PIECE)*4 in column_str: return COMP_PIECE

    for diagRow in range(3):
        for diagCol in range(4):
            square = board[:,diagCol:diagCol+4][diagRow:diagRow+4]
    
            if (np.all(square.diagonal() == square.diagonal()[0])
                    and square.diagonal()[0] in [PLAYER_PIECE, COMP_PIECE]):
                return square.diagonal()[0]
            
            if (np.all(np.flipud(square).diagonal() == np.flipud(square).diagonal()[0])
                    and np.flipud(square).diagonal()[0] in [PLAYER_PIECE, COMP_PIECE]):
                return np.flipud(square).diagonal()[0]

    return 0

def playPiece(board: np.ndarray, piece: int, field: int) -> bool:
    """places a piece on the board if possible

    Args:
        board (np.ndarray): the current game state
        piece (int): the piece needed to be placed
        field (int): the field the where the piece is placed

    Returns:
        bool: true if the piece is placed or not
    """
    column = board[:,field]

    openRow = np.where(column == 0)[0]
    if len(openRow) == 0: return False
    openRow = max(openRow)

    board[openRow,field] = piece
    return True

def evaluateBoard(board: np.ndarray) -> int:
    """returns a score for the given board

    Args:
        board (np.ndarray): the current game state

    Returns:
        int: the score of the board
    """
    winner = checkWinner(board)
    if winner == PLAYER_PIECE: return float('-inf')
    elif winner == COMP_PIECE: return float('inf')
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
                                evaluateBoard, playPiece, areMovesLeft, checkWinner, generateMoves,
                                maxDepth=8, pruning=True, countEvals=True)

if __name__ == "__main__":
    board = np.array([
                [0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0],
            ])
    
    findBestMove(board)
    exit()
    current_PLAYER_PIECE = PLAYER_PIECE
    print(board)
    while areMovesLeft(board) and not checkWinner(board):
        if current_PLAYER_PIECE == PLAYER_PIECE:
            target_field = int(input("field: "))
            while(not playPiece(board, PLAYER_PIECE, target_field)):
                target_field = int(input("NEU field: "))
        else:
            move = findBestMove(board)
            print("AI:",move)
            playPiece(board, COMP_PIECE, move)
            
        print(board)
            
        if current_PLAYER_PIECE == PLAYER_PIECE: current_PLAYER_PIECE = COMP_PIECE
        else: current_PLAYER_PIECE = PLAYER_PIECE
        
    if not checkWinner(board):
        print("Unentschieden")
    else: print(checkWinner(board))