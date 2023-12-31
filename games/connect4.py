import numpy as np

from typing import Generator
from game import Game, timeit

PREDEFINED_PLAYS = None

class connect4(Game):
    def __init__(self, playerOneID: int, playerTwoID:int = 0, firstPlayerStarts:bool = True, trolling:bool = False):
        self.__lastPlayedField = 3
        self.__isTroll = trolling

        board = np.zeros((6,7), dtype=int)        
        super().__init__(board, playerOneID, playerTwoID=playerTwoID, firstPlayerStarts=firstPlayerStarts)

    def generateMoves(self) -> Generator[int, None, None]:
        lower = self.__lastPlayedField
        higher = lower

        yield lower
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
        elif winner == self.playerTwoPiece and self.__isTroll: return kwargs["depth"] * 100000000
        elif winner == self.playerTwoPiece and not self.__isTroll: return (100 - kwargs["depth"]) * 100000000

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
        #Gucken ob der Play schon einmal berechnet wurde
        dataKey = self.getDataKey()
        if dataKey in PREDEFINED_PLAYS:
            return PREDEFINED_PLAYS[dataKey], 0

        #Gibt es eine Reihe die auf jedenfall verhindert werden muss?
        necessaryPlacement = self.checkForNecessaryPlacement()
        if necessaryPlacement >= 0:
            return necessaryPlacement, 0

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

        move, score = self.minimax(maxDepth=depth, countEvals=True)

        #Wenn winning move, direkt spielen
        alreadyWon=score>=100000000
        if alreadyWon:
            self.writeData(dataKey, move)

        return move, score
    
    def countPlayableRows(self) -> int:
        playableRows = 0
        for column in range(7):
            column_str = ''.join(map(str, self.board[:,column]))
            if '0' in column_str: playableRows += 1
        return playableRows
    
    def checkForNecessaryPlacement(self) -> int:
        for field in self.generateMoves():
            couldBePlaced, placedCoordinates = self.playPiece(self.playerOnePiece, field)
            if not couldBePlaced: continue

            if self.checkWinner() == self.playerOnePiece:
                self.board[(placedCoordinates)] = 0
                return field

            self.board[(placedCoordinates)] = 0
        
        return -1

    def getDataKey(self) -> str:
        global PREDEFINED_PLAYS
        key = self.boardToFlatString()
        if self.__isTroll:
            key += "t"
        else:
            key += "n"
        return key

    @timeit
    @staticmethod
    def loadData():
        global PREDEFINED_PLAYS
        data_dict = {}
        with open('data/connect4.txt', 'r') as file:
            for line in file:
                data = line.strip().split(': ')
                if len(data) == 2:
                    key, value = data
                    data_dict[key] = int(value)
        PREDEFINED_PLAYS = data_dict

    @staticmethod
    def writeData(key, value):
        global PREDEFINED_PLAYS
        if key in PREDEFINED_PLAYS: return
        PREDEFINED_PLAYS[key] = value
        with open('data/connect4.txt', 'a') as file:
            file.write(f"{key}: {value}\n")

connect4.loadData()

if __name__ == "__main__":
    selfPlaying = False
    if selfPlaying:
        game = connect4(1,playerTwoID=2,firstPlayerStarts=False)
        print(game)
        print(game.boardToFlatString())

        game.makeTurn(2, 3)
        game.makeTurn(1, 3)
        print(game)
        print(game.boardToFlatString())

    else:
        from random import random
        game = connect4(1,firstPlayerStarts=(random() <= 0.5),trolling=False)
        print(game)
        while game.makeTurn(1, int(input("Field: "))-1, printAIMove=True, offset=1) == -1:
            print(game)
        print(game)
        print(f"winner={game.checkWinner()}")
