import numpy as np

from typing import Callable, Generator

def minimaxAlgo(board: np.ndarray,
                playerPiece: int,
                compPiece: int,
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
            if not playPiece(copiedBoard, compPiece, field): continue
            
            moveValue, _ = minimaxAlgo(copiedBoard,playerPiece, compPiece, evaluate, playPiece, areMovesLeft, checkWinner, generateMoves,
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
            if not playPiece(copiedBoard, playerPiece, field): continue
            
            moveValue, _ = minimaxAlgo(copiedBoard,playerPiece, compPiece, evaluate, playPiece, areMovesLeft, checkWinner, generateMoves,
                                depth=depth+1, isMaximizing=True, alpha=alpha, beta=beta, maxDepth=maxDepth)
            
            #min
            if moveValue < bestValue:
                bestValue = moveValue
                bestMove = field
            beta = min(beta, bestValue)

            if beta <= alpha:
                break
        
        return bestValue, bestMove