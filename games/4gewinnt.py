import numpy as np
import minimax

from typing import Generator


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
        0 1 2 3 4 5 6
    ] as a numpy matrix (7x6)
    Where
        0 is a free space
        1 is PLAYER_PIECE
        2 is COMP_PIECE
"""

def generateMoves() -> Generator[int, None, None]:
    """generates all moves that could be made, even the ones that are not possible

    Yields:
        int: the move
    """    
    for i in [1,5,2,3,4,0,6]:
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
        if '1111' in row_str: return PLAYER_PIECE
        elif '2222' in row_str: return COMP_PIECE

    for column in range(6):
        column_str = ''.join(map(str, board[:,column]))
        if '1111' in column_str: return PLAYER_PIECE
        elif '2222' in column_str: return COMP_PIECE

    for diagRow in range(3):
        for diagCol in range(4):
            square = board[:,diagCol:diagCol+4][diagRow:diagRow+4]
            leftdiag_str = ''.join(map(str,square.diagonal()))
            rightdiag_str = ''.join(map(str,np.flipud(square).diagonal()))

            if '1111' == leftdiag_str: return PLAYER_PIECE
            if '1111' == rightdiag_str: return PLAYER_PIECE
            if '2222' == leftdiag_str: return COMP_PIECE
            if '2222' == rightdiag_str: return COMP_PIECE

    return 0
    
def playPiece(board: np.ndarray, piece: int, field: int) -> tuple[bool, tuple[int, int]]:
    """places a piece on the board if possible

    Args:
        board (np.ndarray): the current game state
        piece (int): the piece needed to be placed
        field (int): the field the where the piece is placed

    Returns:
        bool: true if the piece is placed or not and the coordinates where it was places
    """
    column = board[:,field]

    openRow = np.where(column == 0)[0]
    if len(openRow) == 0: return False, (-1,-1)
    openRow = max(openRow)

    board[openRow,field] = piece
    return True, (openRow, field)

def evaluateBoard(board: np.ndarray) -> int:
    """returns a score for the given board

    Args:
        board (np.ndarray): the current game state

    Returns:
        int: the score of the board
    """
    winner = checkWinner(board)
    if winner == PLAYER_PIECE: return -10000000000
    elif winner == COMP_PIECE: return 10000000000

    score = 0

    #Middle Control
    for row in [2,3,4]:
        score += np.count_nonzero(board[:,row] == COMP_PIECE)

    #Rows
    for row in range(6):
        row_str = ''.join(map(str, board[row]))
        if '1110' in row_str: score -= 100
        if '1101' in row_str: score -= 100
        if '1011' in row_str: score -= 100
        if '0111' in row_str: score -= 100

        if '0222' in row_str: score += 100
        if '2022' in row_str: score += 100
        if '2202' in row_str: score += 100
        if '2220' in row_str: score += 100

    #Columns
    for column in range(6):
        column_str = ''.join(map(str, board[:,column]))
        if '0111' in column_str: score -= 100
        if '0222' in column_str: score += 100

    #Diagonal
    for diagRow in range(3):
        for diagCol in range(4):
            square = board[:,diagCol:diagCol+4][diagRow:diagRow+4]
            leftdiag_str = ''.join(map(str,square.diagonal()))
            rightdiag_str = ''.join(map(str,np.flipud(square).diagonal()))
    
            if '1110' == leftdiag_str: score -= 100
            if '1101' == leftdiag_str: score -= 100
            if '1011' == leftdiag_str: score -= 100
            if '0111' == leftdiag_str: score -= 100

            if '1110' == rightdiag_str: score -= 100
            if '1101' == rightdiag_str: score -= 100
            if '1011' == rightdiag_str: score -= 100
            if '0111' == rightdiag_str: score -= 100

            if '2220' == leftdiag_str: score += 100
            if '2202' == leftdiag_str: score += 100
            if '2022' == leftdiag_str: score += 100
            if '0222' == leftdiag_str: score += 100

            if '2220' == rightdiag_str: score += 100
            if '2202' == rightdiag_str: score += 100
            if '2022' == rightdiag_str: score += 100
            if '0222' == rightdiag_str: score += 100

    return score

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
                                maxDepth=6, pruning=True, countEvals=False)



if __name__ == "__main__":
    board = np.array([
                [0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0],
            ])
    
    print(checkWinner(board))

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