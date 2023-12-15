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

def isMovePossible(board):
    return np.any(board == 0)

def checkWinner(board):
    for i in range(3):
        #Reihe checken
        if np.all(board[i] == board[i][0]):
            return board[i][0]
        #Spalte checken
        if np.all(board[:,i] == board[:,i][0]):
            return board[:,i][0]
    
    #Diagonale checken
    if np.all(board.diagonal() == board.diagonal()[0]):
        return board.diagonal()[0]
    if np.all(np.flipud(board).diagonal() == np.flipud(board).diagonal()[0]):
        return np.flipud(board).diagonal()[0]
    
    return 0


if __name__ == "__main__":
    board = np.array([
                [0,0,1],
                [0,0,0],
                [1,0,0]
            ])
    
    print(checkWinner(board))