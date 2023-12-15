import numpy as np

from typing import Callable

def minimaxAlgo(board: np.ndarray,
                depth: int,
                alpha: int,
                beta: int,
                isMaximizing: bool,
                playerPiece: int,
                compPiece: int,
                evaluate: Callable[[np.ndarray], int],
                playPiece: Callable[[np.ndarray, int, int], bool],
                areMovesLeft: Callable[[np.ndarray], bool],
                checkWinner: Callable[[np.ndarray], int],
                generateMoves,
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
            
            moveValue, _ = minimaxAlgo(copiedBoard, depth + 1, alpha, beta, False,
                                    playerPiece, compPiece, evaluate, playPiece, areMovesLeft, checkWinner, generateMoves, maxDepth=maxDepth)
            
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
            
            moveValue, _ = minimaxAlgo(copiedBoard, depth + 1, alpha, beta, True,
                                    playerPiece, compPiece, evaluate, playPiece, areMovesLeft, checkWinner, generateMoves, maxDepth=maxDepth)
            
            #min
            if moveValue < bestValue:
                bestValue = moveValue
                bestMove = field
            beta = min(beta, bestValue)

            if beta <= alpha:
                break
        
        return bestValue, bestMove