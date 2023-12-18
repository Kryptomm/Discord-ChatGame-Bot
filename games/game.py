import numpy as np

from time import time
from typing import Callable, Generator

def timeit(func):
    def wrapper(*args, **kwargs):
        start_time = time()
        result = func(*args, **kwargs)
        end_time = time()
        execution_time = end_time - start_time
        print(f"{func.__name__} took {execution_time} seconds to execute")
        return result
    return wrapper

class NotPlayersTurn(Exception):
    def __init__(self, message="Its not the specified players turn"):
        self.message = message
        super().__init__(self.message)

class NotPartOfGame(Exception):
    def __init__(self, message="The specified player is not part of the game"):
        self.message = message
        super().__init__(self.message)



class Game():
    def __init__(self, board: np.ndarray, playerOneID: int, playerTwoID: int = 0, firstPlayerStarts: bool = True):
        self.board = board
        self.playerOneID = playerOneID
        self.playerTwoID = playerTwoID

        self.playerOnePiece = 1
        self.playerTwoPiece = 2

        self.isAgainstAI = (playerTwoID == 0)
        self.__EVALS = 0

        self.currentPlayer = playerOneID
        if not firstPlayerStarts:
            self.currentPlayer = playerTwoID
            if self.isAgainstAI:
                move, score = self.findBestMove()
                self.playPiece(self.playerTwoPiece, move)
                self.currentPlayer = self.playerOneID

                self.__lastPlayedField = move

        
    def makeTurn(self, player: int, field: int, printAIMove: bool = True, offset: int = 0) -> int:
        if player not in [self.playerOnePiece, self.playerTwoPiece]:
            raise NotPartOfGame()
        
        if player != self.currentPlayer:
            raise NotPlayersTurn()
        
        if player == self.playerOneID:
            self.playPiece(self.playerOnePiece, field)
            self.currentPlayer = self.playerTwoID
            
        elif player == self.playerTwoID:
            self.playPiece(self.playerTwoPiece, field)
            self.currentPlayer = self.playerOneID

        self.__lastPlayedField = field
        
        winner = self.checkWinner()
        if winner > 0 or not self.areMovesLeft():
            return winner

        if self.isAgainstAI:
            move, score = self.findBestMove()
            self.playPiece(self.playerTwoPiece, move)
            self.currentPlayer = self.playerOneID

            self.__lastPlayedField = move
            alreadyWon=score>=100000000

            if printAIMove:
                AIMove = move + offset
                print(f"{AIMove=} {score=} {alreadyWon=}")

            winner = self.checkWinner()
            if winner > 0 or not self.areMovesLeft():
                return winner

        return -1
        
    def __minimaxAlgo(self,
                depth: int = 0,
                isMaximizing: bool = True,
                alpha: float = float('-inf'),
                beta: float = float('inf'),
                maxDepth: int = 10,
                pruning: bool = True,
                countEvals: bool = False):

        if depth == maxDepth or (not self.areMovesLeft()) or self.checkWinner():
            if countEvals:
                self.__EVALS += 1
            return self.evaluate(depth=depth), None
        
        if isMaximizing:
            bestValue = float('-inf')
            bestMove = 0
            
            for field in self.generateMoves():
                couldBePlaced, placedCoordinates = self.playPiece(self.playerTwoPiece, field)
                if not couldBePlaced: continue
                
                moveValue, _ = self.__minimaxAlgo(depth=depth+1, isMaximizing=False, alpha=alpha, beta=beta, maxDepth=maxDepth, pruning=pruning, countEvals=countEvals)
                
                self.board[(placedCoordinates)] = 0
                #max
                if moveValue > bestValue:
                    bestValue = moveValue
                    bestMove = field
                    
                alpha = max(alpha, bestValue)

                if not pruning: continue
                if beta <= alpha:
                    break
                
            return bestValue, bestMove

        else:
            bestValue = float('inf')
            bestMove = 0
            
            for field in self.generateMoves():
                couldBePlaced, placedCoordinates = self.playPiece(self.playerOnePiece, field)
                if not couldBePlaced: continue
                
                moveValue, _ = self.__minimaxAlgo(depth=depth+1, isMaximizing=True, alpha=alpha, beta=beta, maxDepth=maxDepth, pruning=pruning, countEvals=countEvals)
                
                self.board[(placedCoordinates)] = 0
                #min
                if moveValue < bestValue:
                    bestValue = moveValue
                    bestMove = field
                beta = min(beta, bestValue)

                if not pruning: continue
                if beta <= alpha:
                    break
            
            return bestValue, bestMove
    
    def minimax(self, maxDepth: int = 10, pruning: bool = True, countEvals: bool = False):
        score, move = self.__minimaxAlgo(maxDepth=maxDepth, pruning=pruning, countEvals=countEvals)

        if countEvals:
            print(f"It took {self.__EVALS} evaulations to compute")
            EVALS = 0

        return move, score
    
    def boardToFlatString(self) -> str:
        return ''.join(map(str, self.board.flatten()))

    def __repr__(self) -> str:
        board_str = " "
        color_codes = [37,32,31]
        elements = ["🟪","🟩","🟥"]

        for i in range(len(self.board[0])):
            board_str += str(i+1) + "  "
        board_str += "\n"

        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                elem = self.board[y,x]
                board_str +=  f"\033[{color_codes[elem]}m{elements[elem]}\033[0m"
            
            board_str += "\n"
        
        return board_str