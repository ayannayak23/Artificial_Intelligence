# -*- coding: utf-8 -*-
"""
Hinger Project
Coursework 001 for: CMP-6058A Artificial Intelligence

Task 3: Agent
Implements decision-making strategies using minimax and alpha-beta pruning algorithms.

@author: B9 (1004411839, 100434969, and 100440712)
@date: 20/10/2025

"""

from a1_state import State


class Agent:
    
    # Intelligent agent for Hinger game using minimax or alpha-beta search.
    # Coordinates are zero-indexed: (row, col) with (0,0) at top-left.
    
    
    def __init__(self, size, name="B9"):
        """Initialize agent with board size and name."""
        self.size = size
        self.name = name
        self.nodes_searched = 0
    
    def __str__(self):
        return f"Agent({self.name})"
    
    def move(self, state, mode="alphabeta", depth=4):

        """
        Select best move for current state.
        
        Args:
            state: current State object
            mode: "minimax" or "alphabeta"
            depth: maximum search depth
        
        Returns:
            (row, col) tuple or None if no legal moves
        """

        self.nodes_searched = 0
        legal_moves = self._list_legal_moves(state)
        
        if not legal_moves:
            return None
        
        # Immediate win: take any hinger
        for r, c, is_hinger in legal_moves:
            if is_hinger:
                return (r, c)
        
        # Search
        if mode == "minimax":
            score, best_move = self._minimax(state, depth, True)
        elif mode == "alphabeta":
            score, best_move = self._alphabeta(state, depth, float('-inf'), float('inf'), True)
        else:
            raise ValueError(f"Unknown mode: {mode}")
        
        return best_move
    
    def _list_legal_moves(self, state):

        # Generate legal moves as (row, col, is_hinger) tuples, hingers first.

        moves = []
        current_regions = state.numRegions()
        
        for r in range(len(state.grid)):
            for c in range(len(state.grid[0])):
                if state.grid[r][c] > 0:
                    is_hinger = False
                    if state.grid[r][c] == 1:
                        test_state = state.clone()
                        test_state.grid[r][c] = 0
                        if test_state.numRegions() > current_regions:
                            is_hinger = True
                    moves.append((r, c, is_hinger))
        
        moves.sort(key=lambda x: x[2], reverse=True)
        return moves
    
    def _evaluate(self, state):

        # Heuristic: current hingers minus estimated opponent hingers.

        current_hingers = state.numHingers()
        
        legal_moves = self._list_legal_moves(state)
        max_opp_hingers = 0
        
        for r, c, _ in legal_moves[:3]:
            test_state = state.clone()
            test_state.grid[r][c] -= 1
            max_opp_hingers = max(max_opp_hingers, test_state.numHingers())
        
        return current_hingers - max_opp_hingers
    
    def _minimax(self, state, depth, maximizing):

        # Minimax search returning (score, move).

        self.nodes_searched += 1
        legal_moves = self._list_legal_moves(state)
        
        if depth == 0 or not legal_moves:
            return (self._evaluate(state) if legal_moves else 0, None)
        
        best_move = None
        
        if maximizing:
            max_eval = float('-inf')
            for r, c, is_hinger in legal_moves:
                if is_hinger:
                    return (1, (r, c))
                
                original = state.grid[r][c]
                state.grid[r][c] -= 1
                eval_score, _ = self._minimax(state, depth - 1, False)
                state.grid[r][c] = original
                
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = (r, c)
            return (max_eval, best_move)
        else:
            min_eval = float('inf')
            for r, c, is_hinger in legal_moves:
                if is_hinger:
                    return (-1, (r, c))
                
                original = state.grid[r][c]
                state.grid[r][c] -= 1
                eval_score, _ = self._minimax(state, depth - 1, True)
                state.grid[r][c] = original
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = (r, c)
            return (min_eval, best_move)
    
    def _alphabeta(self, state, depth, alpha, beta, maximizing):

        # Alpha-beta pruning search returning (score, move).
        
        self.nodes_searched += 1
        legal_moves = self._list_legal_moves(state)
        
        if depth == 0 or not legal_moves:
            return (self._evaluate(state) if legal_moves else 0, None)
        
        best_move = None
        
        if maximizing:
            max_eval = float('-inf')
            for r, c, is_hinger in legal_moves:
                if is_hinger:
                    return (1, (r, c))
                
                original = state.grid[r][c]
                state.grid[r][c] -= 1
                eval_score, _ = self._alphabeta(state, depth - 1, alpha, beta, False)
                state.grid[r][c] = original
                
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = (r, c)
                
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return (max_eval, best_move)
        else:
            min_eval = float('inf')
            for r, c, is_hinger in legal_moves:
                if is_hinger:
                    return (-1, (r, c))
                
                original = state.grid[r][c]
                state.grid[r][c] -= 1
                eval_score, _ = self._alphabeta(state, depth - 1, alpha, beta, True)
                state.grid[r][c] = original
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = (r, c)
                
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return (min_eval, best_move)
