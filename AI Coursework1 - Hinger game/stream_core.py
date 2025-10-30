# -*- coding: utf-8 -*-
# Streaming Hinger Game Core
# Shared helpers and play_stream for streamed gameplay with delays

import time
from typing import Optional, Tuple
from a1_state import State
from a3_agent import Agent


def is_legal(state: State, r: int, c: int) -> bool:
    # Check if move at (r,c) is legal (in bounds and cell > 0)
    rows, cols = len(state.grid), len(state.grid[0])
    if r < 0 or r >= rows or c < 0 or c >= cols:
        return False
    return state.grid[r][c] > 0


def is_hinger_now(state: State, r: int, c: int) -> bool:
    # Check if cell at (r,c) is a hinger (value=1 and removal increases regions)
    if state.grid[r][c] != 1:
        return False
    regions_before = state.numRegions()
    # Clone state and test removal
    test = state.clone()
    test.grid[r][c] = 0
    regions_after = test.numRegions()
    return regions_after > regions_before


def apply_move(state: State, r: int, c: int) -> None:
    # Apply move by decrementing cell at (r,c) by 1. Mutates state in place
    state.grid[r][c] -= 1


def board_cleared(state: State) -> bool:
    # Check if board is completely cleared (all cells are 0)
    for row in state.grid:
        for cell in row:
            if cell > 0:
                return False
    return True


def print_board(state: State, title: str, move: Optional[Tuple[int, int]] = None,
                hinger: bool = False, nodes: Optional[int] = None) -> None:
    # Print board with turn title and optional move details
    line = f"\n{title}"
    if move is not None:
        line += f" | move {move}"
        if hinger:
            line += " [HINGER!]"
        if nodes is not None:
            line += f" | {nodes} nodes"
    print(line)
    print(state)


def play_stream(state: State,
                agentA: Optional[Agent],
                agentB: Optional[Agent],
                delay: float = 2.0,
                mode: str = "alphabeta",
                depth: int = 4) -> Optional[str]:
    # Alternating turns with streaming prints and delay
    # Returns winner name or None on draw
    labels = {
        "A": agentA.name if agentA else "Human A",
        "B": agentB.name if agentB else "Human B"
    }
    current = "A"
    hinger_played = False
    
    print_board(state, "Start")
    time.sleep(delay)
    
    while True:
        player = agentA if current == "A" else agentB
        label = labels[current]
        opp = "B" if current == "A" else "A"
        opp_label = labels[opp]
        
        # Choose move: human input or agent decision
        if player is None:
            # Human input
            try:
                s = input(f"{label} move (row col): ").strip()
                parts = s.split()
                if len(parts) != 2 or not all(p.lstrip('-').isdigit() for p in parts):
                    print(f"Invalid input → {opp_label} wins.")
                    return opp_label
                r, c = map(int, parts)
                nodes = None
            except (ValueError, KeyboardInterrupt):
                print(f"Input error → {opp_label} wins.")
                return opp_label
        else:
            # Agent move
            mv = player.move(state, mode=mode, depth=depth)
            if mv is None:
                print(f"{label} has no legal move → {opp_label} wins.")
                return opp_label
            r, c = mv
            nodes = getattr(player, 'nodes_searched', None)
        
        # Legality check
        if not is_legal(state, r, c):
            print(f"Illegal move by {label} at {(r, c)} → {opp_label} wins.")
            return opp_label
        
        # Hinger check BEFORE applying
        is_h = is_hinger_now(state, r, c)
        
        # Apply move to state
        apply_move(state, r, c)
        
        # Show board and pause for visualization
        print_board(state, f"{label} played {(r, c)}", move=(r, c), hinger=is_h, nodes=nodes)
        time.sleep(delay)
        
        # Terminal checks
        if is_h:
            hinger_played = True
            print(f"→ {label} wins by hinger!")
            return label
        
        if board_cleared(state) and not hinger_played:
            print("→ Draw: board cleared, no hinger played.")
            return None
        
        # Switch player
        current = opp
