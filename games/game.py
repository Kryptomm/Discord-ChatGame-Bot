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
    def __init__(self, board: np.ndarray, playerOneID: int, playerTwoID:int = 0):
        self.board = board
        self.playerOneID = playerOneID
        self.playerTwoID = playerTwoID

        self.currentPlayer = playerOneID

        self.playerOnePiece = 1
        self.playerTwoPiece = 2

        self.isAgainstAI = (playerTwoID == 0)

        self.__EVALS = 0

    def makeTurn(self, player: int, field: int) -> bool:
        if player not in [self.playerOnePiece, self.playerTwoPiece]:
            raise NotPartOfGame()
        
        if player != self.currentPlayer:
            raise NotPlayersTurn()
        
        if player == self.playerOneID:
            self.playPiece(self.playerOnePiece, field)
        elif player == self.playerTwoID:
            self.playPiece(self.playerTwoPiece, field)
        
        winner = self.checkWinner()
        if winner > 0 or not self.areMovesLeft():
            return winner

        if self.isAgainstAI:
            move = self.findBestMove()
            self.playPiece(self.playerTwoPiece, move)
        
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
            return self.evaluate(), None
        
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
        move = self.__minimaxAlgo(maxDepth=maxDepth, pruning=pruning, countEvals=countEvals)[1]
        
        if countEvals:
            print(f"It took {self.__EVALS} evaulations to compute")
            EVALS = 0

        return move