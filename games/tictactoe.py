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
    ] as a numpy matrix
    Where
        0 is a free space
        1 is PLAYER_PIECE
        2 is COMP_PIECE
"""

def areMovesLeft(board: np.ndarray) -> bool:
    return np.any(board == 0)

def checkWinner(board: np.ndarray) -> int:
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

def generateMoves():
    for i in range(9):
        yield i

def playPiece(board: np.ndarray, piece: int, field: int) -> bool:
    y = field // 3
    x = field % 3
    
    if board[y][x]: return False
    
    board[y][x] = piece
    return True

def evaluateBoard(board: np.ndarray) -> int:
    winner = checkWinner(board)
    if winner == PLAYER_PIECE: return -1
    elif winner == COMP_PIECE: return 1
    else: return 0

def findBestMove(board: np.ndarray) -> int:
    copiedBoard = np.copy(board)
    return minimax.minimaxAlgo(copiedBoard, 0, float('-inf'), float('inf'), True, PLAYER_PIECE, COMP_PIECE,
                                            evaluateBoard, playPiece, areMovesLeft, checkWinner, generateMoves, maxDepth=20)[1]

if __name__ == "__main__":
    board = np.array([
                [0,0,0],
                [0,0,0],
                [0,0,0]
            ])
    
    current_PLAYER_PIECE = COMP_PIECE
    print(board)
    while areMovesLeft(board) and not checkWinner(board):
        if current_PLAYER_PIECE == PLAYER_PIECE:
            target_field = int(input("field: "))
            while(not playPiece(board, PLAYER_PIECE, target_field)):
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