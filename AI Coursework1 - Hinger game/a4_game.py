# -*- coding: utf-8 -*-
"""
Task 4: Game Loop for Hinger Game
Implements the complete game flow with win/draw/illegal move detection.

@author: Ahmed
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
