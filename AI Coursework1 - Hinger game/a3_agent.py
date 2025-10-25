# -*- coding: utf-8 -*-
"""
Task 3: Agent for Hinger Game
Implements minimax and alpha-beta pruning strategies.

@author: GitHub Copilot
"""

from a1_state import State


class Agent:
    """
    Intelligent agent for Hinger game using minimax or alpha-beta search.
    Coordinates are zero-indexed: (row, col) with (0,0) at top-left.
    """
    
    def __init__(self, size, name="A9"):
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
        """Generate legal moves as (row, col, is_hinger) tuples, hingers first."""
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
        """Heuristic: current hingers minus estimated opponent hingers."""
        current_hingers = state.numHingers()
        
        legal_moves = self._list_legal_moves(state)
        max_opp_hingers = 0
        
        for r, c, _ in legal_moves[:3]:
            test_state = state.clone()
            test_state.grid[r][c] -= 1
            max_opp_hingers = max(max_opp_hingers, test_state.numHingers())
        
        return current_hingers - max_opp_hingers
    
    def _minimax(self, state, depth, maximizing):
        """Minimax search returning (score, move)."""
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
        """Alpha-beta pruning search returning (score, move)."""
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
    """Test Agent with various scenarios."""
    print("=" * 60)
    print("Testing Agent for Hinger Game")
    print("=" * 60)
    
    all_passed = True
    
    # Scenario A: No immediate win
    print("\n--- Scenario A: No Immediate Win ---")
    grid_a = [[0, 1, 1], [1, 0, 1], [1, 1, 1]]
    state_a = State(grid_a, size=3)
    print("Board:")
    print(state_a)
    print(f"Number of hingers: {state_a.numHingers()}")
    
    agent = Agent(size=(3, 3), name="TestAgent")
    
    move_mm = agent.move(state_a, mode="minimax", depth=4)
    print(f"\nMinimax (depth=4): {move_mm}")
    print(f"  Nodes searched: {agent.nodes_searched}")
    if move_mm is None:
        print("  ERROR: Should find a move!")
        all_passed = False
    else:
        print(f"  Selected move at (row={move_mm[0]}, col={move_mm[1]})")
    
    move_ab = agent.move(state_a, mode="alphabeta", depth=4)
    print(f"\nAlpha-beta (depth=4): {move_ab}")
    print(f"  Nodes searched: {agent.nodes_searched}")
    if move_ab is None:
        print("  ERROR: Should find a move!")
        all_passed = False
    else:
        print(f"  Selected move at (row={move_ab[0]}, col={move_ab[1]})")
    
    # Scenario B: Multiple immediate wins
    print("\n" + "=" * 60)
    print("--- Scenario B: Multiple Immediate Wins ---")
    grid_b = [[1, 0, 1], [1, 0, 1], [1, 1, 1]]
    state_b = State(grid_b, size=3)
    print("Board:")
    print(state_b)
    print(f"Number of hingers: {state_b.numHingers()}")
    
    move_mm_b = agent.move(state_b, mode="minimax", depth=4)
    print(f"\nMinimax (depth=4): {move_mm_b}")
    if move_mm_b is None:
        print("  ERROR: Should find a hinger move!")
        all_passed = False
    else:
        r, c = move_mm_b
        if state_b.grid[r][c] == 1:
            test_state = state_b.clone()
            test_state.grid[r][c] = 0
            if test_state.numRegions() > state_b.numRegions():
                print(f"  [OK] Picked hinger at (row={r}, col={c})")
            else:
                print(f"  ERROR: Not a hinger!")
                all_passed = False
    
    move_ab_b = agent.move(state_b, mode="alphabeta", depth=4)
    print(f"\nAlpha-beta (depth=4): {move_ab_b}")
    if move_ab_b is None:
        print("  ERROR: Should find a hinger move!")
        all_passed = False
    else:
        r, c = move_ab_b
        if state_b.grid[r][c] == 1:
            test_state = state_b.clone()
            test_state.grid[r][c] = 0
            if test_state.numRegions() > state_b.numRegions():
                print(f"  [OK] Picked hinger at (row={r}, col={c})")
            else:
                print(f"  ERROR: Not a hinger!")
                all_passed = False
    
    # Scenario C: Neutral midgame
    print("\n" + "=" * 60)
    print("--- Scenario C: Neutral Midgame (No Hingers) ---")
    grid_c = [[2, 2, 0], [2, 2, 2], [0, 2, 2]]
    state_c = State(grid_c, size=3)
    print("Board:")
    print(state_c)
    print(f"Number of hingers: {state_c.numHingers()}")
    
    move_mm_c = agent.move(state_c, mode="minimax", depth=3)
    print(f"\nMinimax (depth=3): {move_mm_c}")
    print(f"  Nodes searched: {agent.nodes_searched}")
    if move_mm_c is None:
        print("  ERROR: Should find a move!")
        all_passed = False
    else:
        print(f"  Selected move at (row={move_mm_c[0]}, col={move_mm_c[1]})")
    
    move_ab_c = agent.move(state_c, mode="alphabeta", depth=3)
    print(f"\nAlpha-beta (depth=3): {move_ab_c}")
    print(f"  Nodes searched: {agent.nodes_searched}")
    if move_ab_c is None:
        print("  ERROR: Should find a move!")
        all_passed = False
    else:
        print(f"  Selected move at (row={move_ab_c[0]}, col={move_ab_c[1]})")
    
    # Summary
    print("\n" + "=" * 60)
    if all_passed:
        print("[OK] All tests PASSED!")
    else:
        print("[X] Some tests FAILED!")
    print("=" * 60)
    
    return all_passed


if __name__ == "__main__":
    tester()
