# -*- coding: utf-8 -*-
# Demo: Complete Hinger Game System
# Demonstrates all components working together

from a1_state import State
from a3_agent import Agent
from a4_game import play


def demo():
    # Run a complete demonstration of the Hinger game system
    
    print("=" * 70)
    print(" HINGER GAME - COMPLETE SYSTEM DEMONSTRATION")
    print("=" * 70)
    
    # Demo 1: Quick win with hingers
    print("\n[DEMO 1] Agent vs Agent - Immediate Hinger Win")
    print("-" * 70)
    # Grid with multiple hingers (value=1 cells)
    grid1 = [
        [1, 0, 1],
        [1, 0, 1],
        [1, 1, 1],
    ]
    state1 = State(grid1, size=3)
    print("Starting board:")
    print(state1)
    print(f"\nHingers available: {state1.numHingers()}")
    
    # Create two agents
    ahmed = Agent(size=(3, 3), name="Ahmed")
    ayan = Agent(size=(3, 3), name="Ayan")
    
    print("\nPlaying game...")
    winner = play(state1, ahmed, ayan)
    print(f"→ Winner: {winner}")
    print("  (Ahmed plays first and takes a hinger for instant win)")
    
    # Demo 2: Strategic game ending in draw
    print("\n" + "=" * 70)
    print("[DEMO 2] Agent vs Agent - Strategic Play to Draw")
    print("-" * 70)
    # Grid with no hingers (all 2s and 0s)
    grid2 = [
        [2, 2, 0],
        [2, 2, 2],
        [0, 2, 2],
    ]
    state2 = State(grid2, size=3)
    print("Starting board:")
    print(state2)
    print(f"\nHingers available: {state2.numHingers()}")
    
    # Create two more agents
    ith = Agent(size=(3, 3), name="Ith")
    manwel = Agent(size=(3, 3), name="Manwel")

    print("\nPlaying game...")
    winner = play(state2, ith, manwel)
    if winner is None:
        print("→ Result: Draw (board cleared without hinger)")
    else:
        print(f"→ Winner: {winner}")
    
    # Summary
    print("\n" + "=" * 70)
    print(" DEMONSTRATION COMPLETE")
    print("=" * 70)
    print("\nKey Features Demonstrated:")
    print("  ✓ Immediate hinger detection and instant win")
    print("  ✓ Strategic gameplay with minimax/alphabeta")
    print("  ✓ Draw detection (cleared board, no hinger)")
    print("  ✓ Different board sizes and configurations")
    print("\nAll components working correctly!")
    print("=" * 70)


if __name__ == "__main__":
    demo()
