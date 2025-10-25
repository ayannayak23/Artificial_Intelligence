# -*- coding: utf-8 -*-
"""
Tests for a3_agent.py Agent class
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from a1_state import State
from a3_agent import Agent


def test_no_immediate_win():
    """Test: No immediate win available."""
    print("\n--- Test A: No Immediate Win ---")
    grid = [[0, 1, 1], [1, 0, 1], [1, 1, 1]]
    state = State(grid, size=3)
    print(f"Board:\n{state}")
    print(f"Hingers: {state.numHingers()}")
    
    agent = Agent(size=(3, 3), name="TestAgent")
    
    move_mm = agent.move(state, mode="minimax", depth=4)
    print(f"Minimax (depth=4): {move_mm}, nodes: {agent.nodes_searched}")
    assert move_mm is not None, "Should find a move"
    
    move_ab = agent.move(state, mode="alphabeta", depth=4)
    print(f"Alpha-beta (depth=4): {move_ab}, nodes: {agent.nodes_searched}")
    assert move_ab is not None, "Should find a move"
    print("[OK] Agent finds moves in neutral position")


def test_multiple_hingers():
    """Test: Multiple immediate wins (hingers) available."""
    print("\n--- Test B: Multiple Immediate Wins ---")
    grid = [[1, 0, 1], [1, 0, 1], [1, 1, 1]]
    state = State(grid, size=3)
    print(f"Board:\n{state}")
    print(f"Hingers: {state.numHingers()}")
    
    agent = Agent(size=(3, 3), name="TestAgent")
    
    move_mm = agent.move(state, mode="minimax", depth=4)
    assert move_mm is not None, "Should find a hinger move"
    r, c = move_mm
    test_state = state.clone()
    test_state.grid[r][c] = 0
    is_hinger = state.grid[r][c] == 1 and test_state.numRegions() > state.numRegions()
    assert is_hinger, f"Move {move_mm} should be a hinger"
    print(f"Minimax picked hinger at {move_mm} [OK]")
    
    move_ab = agent.move(state, mode="alphabeta", depth=4)
    assert move_ab is not None, "Should find a hinger move"
    r, c = move_ab
    test_state = state.clone()
    test_state.grid[r][c] = 0
    is_hinger = state.grid[r][c] == 1 and test_state.numRegions() > state.numRegions()
    assert is_hinger, f"Move {move_ab} should be a hinger"
    print(f"Alpha-beta picked hinger at {move_ab} [OK]")


def test_neutral_midgame():
    """Test: Neutral midgame with no hingers."""
    print("\n--- Test C: Neutral Midgame (No Hingers) ---")
    grid = [[2, 2, 0], [2, 2, 2], [0, 2, 2]]
    state = State(grid, size=3)
    print(f"Board:\n{state}")
    print(f"Hingers: {state.numHingers()}")
    
    agent = Agent(size=(3, 3), name="TestAgent")
    
    move_mm = agent.move(state, mode="minimax", depth=3)
    print(f"Minimax (depth=3): {move_mm}, nodes: {agent.nodes_searched}")
    assert move_mm is not None, "Should find a move"
    
    move_ab = agent.move(state, mode="alphabeta", depth=3)
    print(f"Alpha-beta (depth=3): {move_ab}, nodes: {agent.nodes_searched}")
    assert move_ab is not None, "Should find a move"
    print("[OK] Agent handles neutral midgame")


if __name__ == "__main__":
    print("=" * 60)
    print("a3_agent.py Tests")
    print("=" * 60)
    
    test_no_immediate_win()
    test_multiple_hingers()
    test_neutral_midgame()
    
    print("\n" + "=" * 60)
    print("All tests passed!")
    print("=" * 60)
