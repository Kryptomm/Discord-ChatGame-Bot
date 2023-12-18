import numpy as np

from typing import Generator
from game import Game, timeit

PREDEFINED_PLAYS = None

@timeit
def loadData():
    global PREDEFINED_PLAYS
    data_dict = {}
    with open('data/connect4.txt', 'r') as file:
        for line in file:
            key, value = line.strip().split(': ')
            data_dict[key] = int(value)
    PREDEFINED_PLAYS = data_dict

class connect4(Game):
    def __init__(self, playerOneID: int, playerTwoID:int = 0, firstPlayerStarts:bool = True):
        self.__lastPlayedField = 3

        board = np.zeros((6,7), dtype=int)        
        super().__init__(board, playerOneID, playerTwoID=playerTwoID, firstPlayerStarts=firstPlayerStarts)

    def generateMoves(self) -> Generator[int, None, None]:
        lower = self.__lastPlayedField
        higher = self.__lastPlayedField

        yield self.__lastPlayedField
        while higher < 6 or lower > 0:
            if higher < 6:
                higher += 1
                yield higher
                
            if lower > 0:
                lower -= 1
                yield lower


    def areMovesLeft(self) -> bool:
        return np.any(self.board == 0)
    
    def checkWinner(self) -> int: 
        for row in range(6):
            row_str = ''.join(map(str, self.board[row]))
            if '1111' in row_str: return self.playerOnePiece
            elif '2222' in row_str: return self.playerTwoPiece

        for column in range(7):
            column_str = ''.join(map(str, self.board[:,column]))
            if '1111' in column_str: return self.playerOnePiece
            elif '2222' in column_str: return self.playerTwoPiece

        for diagRow in range(3):
            for diagCol in range(4):
                square = self.board[:,diagCol:diagCol+4][diagRow:diagRow+4]
                leftdiag_str = ''.join(map(str,square.diagonal()))
                rightdiag_str = ''.join(map(str,np.flipud(square).diagonal()))

                if '1111' == leftdiag_str: return self.playerOnePiece
                if '1111' == rightdiag_str: return self.playerOnePiece
                if '2222' == leftdiag_str: return self.playerTwoPiece
                if '2222' == rightdiag_str: return self.playerTwoPiece

        return 0
    
    def playPiece(self, piece: int, field: int) -> tuple[bool, tuple[int, int]]:
        column = self.board[:,field]

        openRow = np.where(column == 0)[0]
        if len(openRow) == 0: return False, (-1,-1)
        openRow = max(openRow)

        self.board[openRow,field] = piece
        return True, (openRow, field)
    
    def evaluate(self, **kwargs) -> int:
        winner = self.checkWinner()
        if winner == self.playerOnePiece: return (100 - kwargs["depth"]) * -100000000 #Zögert Lose raus damit Spieler noch Fehler machen kann
        elif winner == self.playerTwoPiece: return kwargs["depth"] * 100000000 #Nimmt den schnellstmöglichen Win (ohne Diff für trollen von Gegner)

        score = 0

        #Middle Control
        for row in [2,3,4]:
            score += np.count_nonzero(self.board[:,row] == self.playerTwoPiece)

        #Rows
        for row in range(6):
            row_str = ''.join(map(str, self.board[row]))
            if '1110' in row_str: score -= 100
            if '1101' in row_str: score -= 100
            if '1011' in row_str: score -= 100
            if '0111' in row_str: score -= 100

            if '0222' in row_str: score += 100
            if '2022' in row_str: score += 100
            if '2202' in row_str: score += 100
            if '2220' in row_str: score += 100

        #Columns
        for column in range(7):
            column_str = ''.join(map(str, self.board[:,column]))
            if '0111' in column_str: score -= 100
            if '0222' in column_str: score += 100

        #Diagonal
        for diagRow in range(3):
            for diagCol in range(4):
                square = self.board[:,diagCol:diagCol+4][diagRow:diagRow+4]
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
    
    @timeit
    def findBestMove(self) -> int:
        flatBoard = self.boardToFlatString()
        if flatBoard in PREDEFINED_PLAYS:
            return PREDEFINED_PLAYS[flatBoard], 0

        playableRows = self.countPlayableRows()
        #depth dependent from free columns to play
        depth = {
            0: 1000,
            1: 1000,
            2: 19,
            3: 12,
            4: 9,
            5: 8,
            6: 8,
            7: 7
        }[playableRows]

        return self.minimax(maxDepth=depth, countEvals=True)
    
    def countPlayableRows(self) -> int:
        playableRows = 0
        for column in range(7):
            column_str = ''.join(map(str, self.board[:,column]))
            if '0' in column_str: playableRows += 1
        return playableRows
    
    def boardToFlatString(self) -> str:
        return ''.join(map(str, self.board.flatten()))

loadData()

if __name__ == "__main__":
    game = connect4(1,firstPlayerStarts=False)

    print(game)
    while game.makeTurn(1, int(input("Field: "))-1, printAIMove=True, offset=1) == -1:
        print(game)
    print(game)
    print(game.checkWinner())
