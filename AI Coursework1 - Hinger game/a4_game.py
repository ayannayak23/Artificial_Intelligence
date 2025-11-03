# -*- coding: utf-8 -*-
"""
Hinger Project
Coursework 001 for: CMP-6058A Artificial Intelligence

Task 4: Game Loop
Implements the complete game flow with win/draw/illegal move detection.

@author: B9 (1004411839, 100434969, and 100440712)
@date: 20/10/2025
"""

from a1_state import State
from a3_agent import Agent
from stream_core import is_legal, is_hinger_now, apply_move, board_cleared


def play(state, agentA, agentB):
    current = "A"  # which player is to move: "A" or "B"
    players = {"A": agentA, "B": agentB}  # map player id to agent or None
    # Friendly display names for prompts and result messages
    labels = {
        "A": agentA.name if agentA else "Human A",
        "B": agentB.name if agentB else "Human B"
    }
    # Tracks whether a hinger has been played in the game yet
    hinger_played = False
    
    while True:
        # 1) Choose move: either get input from a human or ask the agent
        if players[current] is None:
            # Human turn
            try:
                # Prompt format: two integers separated by space, e.g. "1 2"
                inp = input(f"{labels[current]}'s turn. Enter move as 'row col': ").strip()
                parts = inp.split()
                if len(parts) != 2:
                    # Malformed input counts as an immediate loss for the current player
                    print(f"Invalid input format. {labels['B' if current == 'A' else 'A']} wins!")
                    return labels["B" if current == "A" else "A"]
                r, c = int(parts[0]), int(parts[1])
            except (ValueError, KeyboardInterrupt):
                # Any error while parsing input is treated as a loss for the human
                print(f"Invalid input. {labels['B' if current == 'A' else 'A']} wins!")
                return labels["B" if current == "A" else "A"]
        else:
            # Agent turn
            move = players[current].move(state)
            if move is None:
                # No legal move => opponent wins
                return labels["B" if current == "A" else "A"]
            r, c = move
        
        # 2) Legality check: ensure the chosen cell is a legal move
        if not is_legal(state, r, c):
            # Illegal move detected: by rule the opponent immediately wins
            return labels["B" if current == "A" else "A"]
        
        # 3) Hinger check: determine if this move is a hinger *before* applying it.
        # As per game rules, the hinger property is evaluated on the current
        # board configuration prior to removing the stone.

        is_h = is_hinger_now(state, r, c)
        # Apply the move to mutate the game state (remove the stone / update regions)
        apply_move(state, r, c)

        # 4) Terminal checks: check for immediate win or draw conditions
        if is_h:
            # If a hinger was played, the player instantly wins
            hinger_played = True
            return labels[current]

        # If the board is now empty and no hinger has been played in the game,
        if board_cleared(state) and not hinger_played:
            return None
        
        # 5) Switch player
        current = "B" if current == "A" else "A"


def tester():
    # Test function to validate the play() implementation.
    # Tests game flow, win conditions (hinger), draw detection, and illegal move handling.
    
    print("=" * 60)
    print("a4_game.py Game Tests")
    print("=" * 60)
    
    # Test A: Agent vs Agent with immediate hinger available
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
    
    # Test B: Agent vs Agent with no hingers (draw scenario)
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
    
    # Test C: Illegal move handling
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
    
    print("\n" + "=" * 60)
    print("All tests passed!")
    print("=" * 60)


if __name__ == "__main__":
    tester()
