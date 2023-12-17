import numpy as np

from game import Game


class TicTacToe(Game):
    def __init__(self, playerOneID: int, playerTwoID:int = 0):
        board = np.zeros((3,3), dtype=int)

        super().__init__(board, playerOneID, playerTwoID=playerTwoID)

    def generateMoves(self):
        for i in range(9):
            yield i

    def areMovesLeft(self) -> bool:
        return np.any(self.board == 0)
    
    def checkWinner(self) -> int:
        for i in range(3):
            #Check Rows
            if np.all(self.board[i] == self.board[i][0]):
                return self.board[i][0]
            #Check Columns
            if np.all(self.board[:,i] == self.board[:,i][0]):
                return self.board[:,i][0]
        
        #Check diagonals
        if np.all(self.board.diagonal() == self.board.diagonal()[0]):
            return self.board.diagonal()[0]
        if np.all(np.flipud(self.board).diagonal() == np.flipud(self.board).diagonal()[0]):
            return np.flipud(self.board).diagonal()[0]
        
        #No winner
        return 0
    
    def playPiece(self, piece: int, field: int) -> tuple[bool, tuple[int, int]]:
        y = field // 3
        x = field % 3
        
        if self.board[y,x]: return False, (-1, -1)
        
        self.board[y,x] = piece
        return True, (y,x)
    
    def evaluate(self) -> int:
        winner = self.checkWinner()
        if winner == self.playerOnePiece: return -1
        elif winner == self.playerTwoPiece: return 1
        else: return 0

        
    def findBestMove(self) -> int:
        return self.minimax()


if __name__ == "__main__":
    game = TicTacToe(1,0)
    
    game.makeTurn(1,0)
    print(game.board)

    game.makeTurn(1,8)
    print(game.board)