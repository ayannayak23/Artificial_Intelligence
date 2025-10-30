# -*- coding: utf-8 -*-
# Tests for a4_game.py play() function
# Verifies game flow, win conditions, and illegal move handling

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from a1_state import State
from a3_agent import Agent
from a4_game import play


def test_immediate_hinger():
    # Test: Agent vs Agent with immediate hinger available
    # First player (AgentA) should win by taking hinger immediately
    print("\n--- Test A: Immediate Hinger ---")
    grid = [
        [1, 0, 1],
        [1, 0, 1],
        [1, 1, 1],
    ]
    state = State(grid, size=3)
    print(f"Initial board:\n{state}")
    print(f"Hingers: {state.numHingers()}")
    
    agentA = Agent(size=(3, 3), name="AgentA")
    agentB = Agent(size=(3, 3), name="AgentB")
    
    winner = play(state, agentA, agentB)
    print(f"Result: {winner}")
    assert winner == "AgentA", f"Expected AgentA, got {winner}"
    print("[OK] AgentA wins by playing hinger immediately")


def test_draw():
    # Test: Agent vs Agent with no hingers (draw scenario)
    # Board gets cleared without any hinger being played -> draw
    print("\n--- Test B: Draw (No Hingers) ---")
    grid = [
        [2, 2, 0],
        [2, 2, 2],
        [0, 2, 2],
    ]
    state = State(grid, size=3)
    print(f"Initial board:\n{state}")
    print(f"Hingers: {state.numHingers()}")
    
    agentC = Agent(size=(3, 3), name="AgentC")
    agentD = Agent(size=(3, 3), name="AgentD")
    
    winner = play(state, agentC, agentD)
    print(f"Result: {'Draw' if winner is None else winner}")
    assert winner is None, f"Expected Draw (None), got {winner}"
    print("[OK] Draw: board cleared without hinger")


def test_illegal_move():
    # Test: Illegal move handling
    # DummyAgent makes out-of-bounds move -> opponent wins
    print("\n--- Test C: Illegal Move Handling ---")
    
    class DummyAgent:
        # Agent that always returns illegal move (out of bounds)
        def __init__(self, name="Dummy"):
            self.name = name
        
        def move(self, state):
            return (-1, 99)  # Intentionally illegal coordinates
    
    grid = [
        [1, 1],
        [1, 1],
    ]
    state = State(grid, size=2)
    print(f"Initial board:\n{state}")
    
    dummy = DummyAgent(name="BadAgent")
    agentE = Agent(size=(2, 2), name="GoodAgent")
    
    # DummyAgent plays first but makes illegal move
    winner = play(state, dummy, agentE)
    print(f"Result: {winner}")
    assert winner == "GoodAgent", f"Expected GoodAgent, got {winner}"
    print("[OK] GoodAgent wins (BadAgent made illegal move)")


if __name__ == "__main__":
    # Run all game tests
    print("=" * 60)
    print("a4_game.py Tests")
    print("=" * 60)
    
    test_immediate_hinger()
    test_draw()
    test_illegal_move()
    
    print("\n" + "=" * 60)
    print("All tests passed!")
    print("=" * 60)
