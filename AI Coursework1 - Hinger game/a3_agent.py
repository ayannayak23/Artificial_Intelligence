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


def tester():
    # Test function to demonstrate and validate agent behavior across scenarios.
    # Tests minimax and alphabeta move selection in various board configurations.
    
    print("=" * 60)
    print("a3_agent.py Agent Tests")
    print("=" * 60)
    
    # Test A: No immediate win available - agent must search deeper
    print("\n--- Test A: No Immediate Win ---")
    # Grid with value=1 cells but none are hingers (no region increase)
    grid = [[0, 1, 1], [1, 0, 1], [1, 1, 1]]
    state = State(grid, size=3)
    print(f"Board:\n{state}")
    print(f"Hingers: {state.numHingers()}")
    
    agent = Agent(size=(3, 3), name="TestAgent")
    
    # Test minimax at depth 4
    move_mm = agent.move(state, mode="minimax", depth=4)
    print(f"Minimax (depth=4): {move_mm}, nodes: {agent.nodes_searched}")
    assert move_mm is not None, "Should find a move"
    
    # Test alphabeta at depth 4 (should be faster due to pruning)
    move_ab = agent.move(state, mode="alphabeta", depth=4)
    print(f"Alpha-beta (depth=4): {move_ab}, nodes: {agent.nodes_searched}")
    assert move_ab is not None, "Should find a move"
    print("[OK] Agent finds moves in neutral position")
    
    # Test B: Multiple immediate wins (hingers) available - agent should pick one
    print("\n--- Test B: Multiple Immediate Wins ---")
    # Grid with several value=1 cells that increase regions when removed
    grid = [[1, 0, 1], [1, 0, 1], [1, 1, 1]]
    state = State(grid, size=3)
    print(f"Board:\n{state}")
    print(f"Hingers: {state.numHingers()}")
    
    agent = Agent(size=(3, 3), name="TestAgent")
    
    # Minimax should pick a hinger
    move_mm = agent.move(state, mode="minimax", depth=4)
    assert move_mm is not None, "Should find a hinger move"
    r, c = move_mm
    # Verify it's actually a hinger (value=1 and increases regions)
    test_state = state.clone()
    test_state.grid[r][c] = 0
    is_hinger = state.grid[r][c] == 1 and test_state.numRegions() > state.numRegions()
    assert is_hinger, f"Move {move_mm} should be a hinger"
    print(f"Minimax picked hinger at {move_mm} [OK]")
    
    # Alpha-beta should also pick a hinger
    move_ab = agent.move(state, mode="alphabeta", depth=4)
    assert move_ab is not None, "Should find a hinger move"
    r, c = move_ab
    test_state = state.clone()
    test_state.grid[r][c] = 0
    is_hinger = state.grid[r][c] == 1 and test_state.numRegions() > state.numRegions()
    assert is_hinger, f"Move {move_ab} should be a hinger"
    print(f"Alpha-beta picked hinger at {move_ab} [OK]")
    
    # Test C: Neutral midgame with no hingers - strategic decision needed
    print("\n--- Test C: Neutral Midgame (No Hingers) ---")
    # Grid with only value=2 cells and zeros (no hingers possible)
    grid = [[2, 2, 0], [2, 2, 2], [0, 2, 2]]
    state = State(grid, size=3)
    print(f"Board:\n{state}")
    print(f"Hingers: {state.numHingers()}")
    
    agent = Agent(size=(3, 3), name="TestAgent")
    
    # Test with lower depth (3) for reasonable performance
    move_mm = agent.move(state, mode="minimax", depth=3)
    print(f"Minimax (depth=3): {move_mm}, nodes: {agent.nodes_searched}")
    assert move_mm is not None, "Should find a move"
    
    move_ab = agent.move(state, mode="alphabeta", depth=3)
    print(f"Alpha-beta (depth=3): {move_ab}, nodes: {agent.nodes_searched}")
    assert move_ab is not None, "Should find a move"
    print("[OK] Agent handles neutral midgame")
    
    print("\n" + "=" * 60)
    print("All tests passed!")
    print("=" * 60)


if __name__ == "__main__":
    tester()
