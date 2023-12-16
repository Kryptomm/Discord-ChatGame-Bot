import numpy as np
import time

from typing import Callable, Generator
from functools import wraps

EVALS = 0

def timeit(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"{func.__name__} took {execution_time} seconds to execute")
        return result
    return wrapper

def __minimaxAlgo(board: np.ndarray,
                minimizingPiece: int,
                maximizingPiece: int,
                evaluate: Callable[[np.ndarray], int],
                playPiece: Callable[[np.ndarray, int, int], bool],
                areMovesLeft: Callable[[np.ndarray], bool],
                checkWinner: Callable[[np.ndarray], int],
                generateMoves: Generator[int, None, None],
                depth: int = 0,
                isMaximizing: bool = True,
                alpha: float = float('-inf'),
                beta: float = float('inf'),
                maxDepth: int = 10,
                pruning: bool = True,
                countEvals: bool = False):
    """Finds the best move for a given game

    Args:
        board (np.ndarray): The original game state
        minimizingPiece (int): The Piece the player should be (minimizing player)
        maximizingPiece (int): The Piece the computer should be (maximizing player)
        evaluate (Callable[[np.ndarray], int]): a function to evaluate a board state and assings a value to it
        playPiece (Callable[[np.ndarray, int, int], bool]): a function that places a piece on the board if possible
        areMovesLeft (Callable[[np.ndarray], bool]): a function that determines if a game finished
        checkWinner (Callable[[np.ndarray], int]): a function that returns the winner of a game
        generateMoves (Generator[int, None, None]): a function that returns every possible move, even if it is not possible (tictactoe: 0-8)
        depth (int, optional): current depth of the search tree. Defaults to 0.
        isMaximizing (bool, optional): current player. Defaults to True.
        alpha (float, optional): alpha value. Defaults to float('-inf').
        beta (float, optional): beta value. Defaults to float('inf').
        maxDepth (int, optional): max depth to search since search could be infinite. Defaults to 10.
        pruning (bool, optional): is pruning turned on
        countEvals (bool, optional): counts the amount of evaluations

    Returns:
        [int, int]: (maxValue, bestMove) the best move that is also contained in the generateMoves function since it has to be generated from it
    """

    if depth == maxDepth or (not areMovesLeft(board)) or checkWinner(board):
        if countEvals:
            global EVALS
            EVALS += 1
        return evaluate(board), None
    
    if isMaximizing:
        bestValue = float('-inf')
        bestMove = 0
        
        for field in generateMoves():
            couldBePlaced, placedCoordinates = playPiece(board, maximizingPiece, field)
            if not couldBePlaced: continue
            
            moveValue, _ = __minimaxAlgo(board,minimizingPiece, maximizingPiece, evaluate, playPiece, areMovesLeft, checkWinner, generateMoves,
                                depth=depth+1, isMaximizing=False, alpha=alpha, beta=beta, maxDepth=maxDepth, pruning=pruning, countEvals=countEvals)
            
            board[(placedCoordinates)] = 0
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
        
        for field in generateMoves():
            couldBePlaced, placedCoordinates = playPiece(board, minimizingPiece, field)
            if not couldBePlaced: continue
            
            moveValue, _ = __minimaxAlgo(board,minimizingPiece, maximizingPiece, evaluate, playPiece, areMovesLeft, checkWinner, generateMoves,
                                depth=depth+1, isMaximizing=True, alpha=alpha, beta=beta, maxDepth=maxDepth, pruning=pruning, countEvals=countEvals)
            
            board[(placedCoordinates)] = 0
            #min
            if moveValue < bestValue:
                bestValue = moveValue
                bestMove = field
            beta = min(beta, bestValue)

            if not pruning: continue
            if beta <= alpha:
                break
        
        return bestValue, bestMove

@timeit
def minimaxAlgo(board: np.ndarray,
                minimizingPiece: int,
                maximizingPiece: int,
                evaluate: Callable[[np.ndarray], int],
                playPiece: Callable[[np.ndarray, int, int], bool],
                areMovesLeft: Callable[[np.ndarray], bool],
                checkWinner: Callable[[np.ndarray], int],
                generateMoves: Generator[int, None, None],
                maxDepth: int = 10,
                pruning: bool = True,
                countEvals: bool = False):
    """Finds the best move for a given game

    Args:
        board (np.ndarray): The original game state
        minimizingPiece (int): The Piece the player should be (minimizing player)
        maximizingPiece (int): The Piece the computer should be (maximizing player)
        evaluate (Callable[[np.ndarray], int]): a function to evaluate a board state and assings a value to it
        playPiece (Callable[[np.ndarray, int, int], bool]): a function that places a piece on the board if possible
        areMovesLeft (Callable[[np.ndarray], bool]): a function that determines if a game finished
        checkWinner (Callable[[np.ndarray], int]): a function that returns the winner of a game
        generateMoves (Generator[int, None, None]): a function that returns every possible move, even if it is not possible (tictactoe: 0-8)
        maxDepth (int, optional): max depth to search since search could be infinite. Defaults to 10.
        pruning (bool, optional): is pruning turned on
        countEvals (bool, optional): counts the amount of evaluations

    Returns:
        int: the best move that is also contained in the generateMoves function since it has to be generated from it
    """
    
    move = __minimaxAlgo(board, minimizingPiece, maximizingPiece,
                                evaluate, playPiece, areMovesLeft, checkWinner, generateMoves,
                                maxDepth=maxDepth, pruning=pruning, countEvals=countEvals)[1]
    
    if countEvals:
        global EVALS
        print(f"It took {EVALS} evaulations to compute")
        EVALS = 0

    return move