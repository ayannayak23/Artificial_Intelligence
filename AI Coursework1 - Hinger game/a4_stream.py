# -*- coding: utf-8 -*-
"""
Streamed Hinger Game Runner
Displays the board after each move with configurable delay.

@author: GitHub Copilot
"""

import time
from typing import Optional, Tuple
from a1_state import State
from a3_agent import Agent


def play_stream(state: State,
                agentA: Optional[Agent],
                agentB: Optional[Agent],
                delay: float = 2.0,
                default_mode: str = "alphabeta",
                default_depth: int = 4) -> Optional[str]:
    """
    Stream a Hinger game to the terminal, updating the board after each move.

    Args:
        state: current game State (mutated in-place).
        agentA: Agent for A (or None for human A).
        agentB: Agent for B (or None for human B).
        delay: seconds to wait between moves when streaming.
        default_mode: strategy passed to Agent.move(...).
        default_depth: depth passed to Agent.move(...).

    Returns:
        winner_name (str) if someone wins by playing a hinger or via opponent illegal move;
        None if the board is cleared with no hinger ever played (draw).
    """
    labels = {
        "A": agentA.name if agentA else "Human A",
        "B": agentB.name if agentB else "Human B"
    }
    current = "A"
    hinger_played = False
    
    # Initial board display
    _print_board(state, turn_label="Start")
    time.sleep(delay)
    
    while True:
        player = agentA if current == "A" else agentB
        label = labels[current]
        opp = "B" if current == "A" else "A"
        opp_label = labels[opp]
        
        # 1) Choose move (agent or human)
        if player is None:
            # Human input: "r c"
            s = input(f"{label} move (row col): ").strip()
            parts = s.split()
            if len(parts) != 2 or not all(p.lstrip('-').isdigit() for p in parts):
                print(f"Illegal input -> {opp_label} wins.")
                return opp_label
            r, c = map(int, parts)
            nodes = None
        else:
            # Agent move
            mv = player.move(state, mode=default_mode, depth=default_depth)
            if mv is None:
                print(f"{label} returned no move -> {opp_label} wins.")
                return opp_label
            r, c = mv
            nodes = player.nodes_searched
        
        # 2) Legality check
        if not _is_legal(state, r, c):
            print(f"Illegal move by {label} at {(r,c)} -> {opp_label} wins.")
            return opp_label
        
        # 3) Hinger check BEFORE applying
        is_h = _is_hinger_now(state, r, c)
        
        # 4) Apply move
        _apply(state, r, c)
        
        # 5) Show board and pause
        _print_board(state, turn_label=f"{label} played {(r,c)}",
                     move=(r, c), is_hinger=is_h, nodes=nodes)
        time.sleep(delay)
        
        # 6) Terminal checks
        if is_h:
            hinger_played = True
            print(f"→ Instant win! {label} played a hinger.")
            return label
        
        if _board_cleared(state) and not hinger_played:
            print("→ Draw: board cleared without any hinger played.")
            return None
        
        # 7) Switch player
        current = opp


def _print_board(state, turn_label, move: Optional[Tuple[int, int]] = None,
                 is_hinger: bool = False, nodes: Optional[int] = None):
    """
    Print the current board state with turn information.
    
    Args:
        state: State object
        turn_label: description of current turn/move
        move: (row, col) tuple if a move was just made
        is_hinger: True if the move was on a hinger
        nodes: number of nodes searched (for agent moves)
    """
    print("\n" + "=" * 60)
    print(f"Turn: {turn_label}")
    if move is not None:
        info = f"Move: {move}"
        if is_hinger:
            info += " [HINGER!]"
        if nodes is not None:
            info += f" (searched {nodes} nodes)"
        print(info)
    print("-" * 60)
    print(state)
    print("=" * 60)


def _is_legal(state, r, c) -> bool:
    """
    Check if a move at (r, c) is legal.
    
    Args:
        state: State object
        r, c: zero-indexed coordinates
    
    Returns:
        True if legal (in bounds and cell > 0), False otherwise
    """
    rows, cols = len(state.grid), len(state.grid[0])
    
    # Check bounds
    if r < 0 or r >= rows or c < 0 or c >= cols:
        return False
    
    # Check if cell is active (> 0)
    if state.grid[r][c] <= 0:
        return False
    
    return True


def _is_hinger_now(state, r, c) -> bool:
    """
    Check if the cell at (r, c) is a hinger at this moment.
    
    Args:
        state: State object
        r, c: zero-indexed coordinates
    
    Returns:
        True if this cell is a hinger (value=1 and removal increases regions)
    """
    # Only cells with value 1 can be hingers
    if state.grid[r][c] != 1:
        return False
    
    # Compute current regions
    regions_before = state.numRegions()
    
    # Clone and remove the cell
    test_state = state.clone()
    test_state.grid[r][c] = 0
    regions_after = test_state.numRegions()
    
    # Hinger if removal increases regions
    return regions_after > regions_before


def _apply(state, r, c):
    """
    Apply a move by decrementing the cell at (r, c) by 1.
    Mutates the state in place.
    
    Args:
        state: State object
        r, c: zero-indexed coordinates
    """
    state.grid[r][c] -= 1


def _board_cleared(state) -> bool:
    """
    Check if the board is completely cleared (all cells are 0).
    
    Args:
        state: State object
    
    Returns:
        True if all cells are 0, False otherwise
    """
    for row in state.grid:
        for cell in row:
            if cell > 0:
                return False
    return True


def _demo_5x5_agents():
    """Demo: Agent vs Agent on a 5x5 board with streaming output."""
    # 5x5 starting grid (mixed values to produce multiple plies)
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
    
    print("Starting 5x5 board:")
    print(state)
    print(f"Initial hingers: {state.numHingers()}\n")
    
    # Use depth=3 for 5x5 to avoid deep recursion
    winner = play_stream(state, A, B, delay=2.0, default_mode="alphabeta", default_depth=3)
    print(f"\nFinal result: Winner = {winner}")


def _demo_5x5_human_vs_agent():
    """Demo: Human vs Agent on a 5x5 board with streaming output."""
    grid = [
        [2, 1, 0, 1, 2],
        [1, 2, 1, 2, 1],
        [0, 1, 2, 1, 0],
        [1, 2, 1, 2, 1],
        [2, 1, 0, 1, 2],
    ]
    state = State(grid, size=5)
    ai = Agent(size=(5, 5), name="AI")
    
    print("Starting 5x5 board:")
    print(state)
    print(f"Initial hingers: {state.numHingers()}")
    print("\nYou are playing as Human A. AI is AgentB.")
    print("Enter moves as 'row col' (zero-indexed, e.g., '0 0' for top-left)\n")
    
    # Use depth=3 for 5x5 to avoid deep recursion
    winner = play_stream(state, None, ai, delay=1.5, default_mode="alphabeta", default_depth=3)
    print(f"\nFinal result: Winner = {winner}")


if __name__ == "__main__":
    print("=" * 60)
    print(" Streamed 5x5 Agent vs Agent (updates every 2 seconds)")
    print("=" * 60)
    _demo_5x5_agents()
    
