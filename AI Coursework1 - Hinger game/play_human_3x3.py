# -*- coding: utf-8 -*-
"""
Hinger Project
Coursework 001 for: CMP-6058A Artificial Intelligence

Human vs Agent Streamed Game
Runs a 3x3 streamed Hinger game: human (A) vs agent (B) with automated moves.

@author: B9 (1004411839, 100434969, and 100440712)
@date: 20/10/2025
"""

from a1_state import State
from a3_agent import Agent
from stream_core import play_stream


def main():
    # Run Human (A) vs Agent (B) on 3x3 board with streaming output
    # 3x3 grid with no hingers (all 2s and 0s)
    grid = [
        [2, 2, 0],
        [2, 2, 2],
        [0, 2, 2],
    ]
    state = State(grid, size=3)
    # Create bot agent for player B
    bot = Agent(size=(3, 3), name="Bot")

    print("=" * 60)
    print("Human (A) vs Agent (B) — 3x3 (updates every 2s)")
    print("=" * 60)
    print("Enter moves as: row col  (zero-indexed)")
    print("Example: '0 0' for top-left, '2 2' for bottom-right")
    print("=" * 60)
    print(state)
    print()

    # Human plays as A (None), bot plays as B, 2-second delays
    winner = play_stream(state, None, bot, delay=2.0, mode="alphabeta", depth=3)

    # Show final result
    print("\n" + "=" * 60)
    print("Result:", "Draw" if winner is None else f"Winner: {winner}")
    print("=" * 60)


if __name__ == "__main__":
    main()
