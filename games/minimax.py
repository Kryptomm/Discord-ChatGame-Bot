import numpy as np

from typing import Callable, Generator

def minimaxAlgo(board: np.ndarray,
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
                maxDepth: int = 10):
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

    Returns:
        [int, int]: (maxValue, bestMove) the best move that is also contained in the generateMoves function since it has to be generated from it
    """

    if depth == maxDepth:
        return evaluate(board), None
    if not areMovesLeft(board):
        return evaluate(board), None
    if checkWinner(board):
        return evaluate(board), None
    
    if isMaximizing:
        bestValue = float('-inf')
        bestMove = 0
        
        for field in generateMoves():
            copiedBoard = np.copy(board)
            if not playPiece(copiedBoard, maximizingPiece, field): continue
            
            moveValue, _ = minimaxAlgo(copiedBoard,minimizingPiece, maximizingPiece, evaluate, playPiece, areMovesLeft, checkWinner, generateMoves,
                                depth=depth+1, isMaximizing=False, alpha=alpha, beta=beta, maxDepth=maxDepth)
            
            #max
            if moveValue > bestValue:
                bestValue = moveValue
                bestMove = field
                
            alpha = max(alpha, bestValue)

            if beta <= alpha:
                break
            
        return bestValue, bestMove

    else:
        bestValue = float('inf')
        bestMove = 0
        
        for field in generateMoves():
            copiedBoard = np.copy(board)
            if not playPiece(copiedBoard, minimizingPiece, field): continue
            
            moveValue, _ = minimaxAlgo(copiedBoard,minimizingPiece, maximizingPiece, evaluate, playPiece, areMovesLeft, checkWinner, generateMoves,
                                depth=depth+1, isMaximizing=True, alpha=alpha, beta=beta, maxDepth=maxDepth)
            
            #min
            if moveValue < bestValue:
                bestValue = moveValue
                bestMove = field
            beta = min(beta, bestValue)

            if beta <= alpha:
                break
        
        return bestValue, bestMove