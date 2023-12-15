import numpy as np




PLAYER_ONE = 1
PLAYER_TWO = 2

"""
Board is classicly build like this:
    [
        [0,2,0],
        [1,0,1],
        [1,2,2]
    ] as a numpy matrix
    Where
        0 is a free space
        1 is Player_One
        2 is Player_Two
"""

def areMovesLeft(board: np.ndarray) -> bool:
    return np.any(board == 0)

def checkWinner(board: np.ndarray) -> bool:
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

def playPiece(board: np.ndarray, piece: int, field: int) -> bool:
    y = field // 3
    x = field % 3
    
    if board[y][x]: return False
    
    board[y][x] = piece
    return True

if __name__ == "__main__":
    board = np.array([
                [0,0,0],
                [0,0,0],
                [0,0,0]
            ])
    
    current_player = PLAYER_ONE
    while areMovesLeft(board) and not checkWinner(board):
        print(board)
        
        target_field = int(input("field: "))
        while(not playPiece(board, current_player, target_field)):
            target_field = int(input("NEU field: "))
            
        if current_player == PLAYER_ONE: current_player = PLAYER_TWO
        else: current_player = PLAYER_ONE
        
    if not checkWinner(board):
        print("Unentschieden")
    else: print(checkWinner(board))