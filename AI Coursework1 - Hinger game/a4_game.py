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
    """
    Simulate a complete Hinger game on the given State.

    Args:
        state: a State instance (current board).
        agentA: Agent instance or None (None => human turn for A).
        agentB: Agent instance or None (None => human turn for B).

    Returns:
        winner_name: str | None
            - str: the .name of the winning agent/human label if someone wins
                   (by playing a hinger or via opponent illegal move)
            - None: if the board is cleared with no hinger ever played (draw)
    """
    current = "A"
    players = {"A": agentA, "B": agentB}
    labels = {
        "A": agentA.name if agentA else "Human A",
        "B": agentB.name if agentB else "Human B"
    }
    hinger_played = False
    
    while True:
        # 1) Choose move
        if players[current] is None:
            # Human turn
            try:
                inp = input(f"{labels[current]}'s turn. Enter move as 'row col': ").strip()
                parts = inp.split()
                if len(parts) != 2:
                    print(f"Invalid input format. {labels['B' if current == 'A' else 'A']} wins!")
                    return labels["B" if current == "A" else "A"]
                r, c = int(parts[0]), int(parts[1])
            except (ValueError, KeyboardInterrupt):
                print(f"Invalid input. {labels['B' if current == 'A' else 'A']} wins!")
                return labels["B" if current == "A" else "A"]
        else:
            # Agent turn
            move = players[current].move(state)
            if move is None:
                # No legal move => opponent wins
                return labels["B" if current == "A" else "A"]
            r, c = move
        
        # 2) Legality check
        if not is_legal(state, r, c):
            # Illegal => opponent wins
            return labels["B" if current == "A" else "A"]
        
        # 3) Hinger check BEFORE applying (per definition at time of play)
        is_h = is_hinger_now(state, r, c)
        apply_move(state, r, c)
        
        # 4) Terminal checks
        if is_h:
            hinger_played = True
            return labels[current]  # Instant win
        
        if board_cleared(state) and not hinger_played:
            return None  # Draw
        
        # 5) Switch player
        current = "B" if current == "A" else "A"
