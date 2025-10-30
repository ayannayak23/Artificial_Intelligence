# -*- coding: utf-8 -*-
"""
Hinger Project
Coursework 001 for: CMP-6058A Artificial Intelligence

Agent vs Agent Streamed Game (5x5)
Demonstrates a 5x5 Hinger game between two agents.

@author: B9 (1004411839, 100434969, and 100440712)
@date: 20/10/2025
"""

from a1_state import State
from a3_agent import Agent
from stream_core import play_stream


def main():
    # Run Agent vs Agent on 5x5 board with streaming output
    # 5x5 grid with mix of 0s, 1s (hingers), and 2s
    grid = [
        [2, 1, 0, 1, 2],
        [1, 2, 1, 2, 1],
        [0, 1, 2, 1, 0],
        [1, 2, 1, 2, 1],
        [2, 1, 0, 1, 2],
    ]
    state = State(grid, size=5)
    # Create two agents with alphabeta search
    A = Agent(size=(5, 5), name="AgentA")
    B = Agent(size=(5, 5), name="AgentB")
    
    print("=" * 60)
    print("Agent vs Agent — 5x5 (updates every 1s)")
    print("=" * 60)
    print(state)
    print()
    
    # Play with 1-second delay between moves, depth=3 for reasonable speed
    winner = play_stream(state, A, B, delay=1, mode="alphabeta", depth=3)
    
    # Display final result
    print("\n" + "=" * 60)
    print("Winner:", winner if winner else "Draw")
    print("=" * 60)


if __name__ == "__main__":
    main()
