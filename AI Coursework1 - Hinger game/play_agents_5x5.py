# -*- coding: utf-8 -*-
"""
Agent vs Agent — 5x5 Streamed Game
"""

from a1_state import State
from a3_agent import Agent
from stream_core import play_stream


def main():
    """Run Agent vs Agent on 5x5 board with streaming output."""
    grid = [
        [2, 1, 0, 1, 2],
        [1, 2, 1, 2, 1],
        [0, 1, 2, 1, 0],
        [1, 2, 1, 2, 1],
        [2, 1, 0, 1, 2],
    ]
    state = State(grid, size=5)
    A = Agent(size=(5, 5), name="AgentA")
    B = Agent(size=(5, 5), name="AgentB")
    
    print("=" * 60)
    print("Agent vs Agent — 5x5 (updates every 1s)")
    print("=" * 60)
    print(state)
    print()
    
    winner = play_stream(state, A, B, delay=1, mode="alphabeta", depth=3)
    
    print("\n" + "=" * 60)
    print("Winner:", winner if winner else "Draw")
    print("=" * 60)


if __name__ == "__main__":
    main()
