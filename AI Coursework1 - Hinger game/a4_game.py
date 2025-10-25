# -*- coding: utf-8 -*-
"""
Task 4: Game Loop for Hinger Game
Implements the complete game flow with win/draw/illegal move detection.

@author: GitHub Copilot
"""

from a1_state import State
from a3_agent import Agent


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
        if not _move_is_legal(state, r, c):
            # Illegal => opponent wins
            return labels["B" if current == "A" else "A"]
        
        # 3) Hinger check BEFORE applying (per definition at time of play)
        is_h = _is_hinger_now(state, r, c)
        _apply_move(state, r, c)
        
        # 4) Terminal checks
        if is_h:
            hinger_played = True
            return labels[current]  # Instant win
        
        if _board_is_clear(state) and not hinger_played:
            return None  # Draw
        
        # 5) Switch player
        current = "B" if current == "A" else "A"


def _move_is_legal(state, r, c):
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


def _is_hinger_now(state, r, c):
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


def _apply_move(state, r, c):
    """
    Apply a move by decrementing the cell at (r, c) by 1.
    Mutates the state in place.
    
    Args:
        state: State object
        r, c: zero-indexed coordinates
    """
    state.grid[r][c] -= 1


def _board_is_clear(state):
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


def tester():
    """
    Test the play() function with various scenarios.
    
    Returns:
        True if all tests complete without errors
    """
    print("=" * 60)
    print("=== a4_game tester ===")
    print("=" * 60)
    
    # --- Scenario A: Agent vs Agent with immediate hingers ---
    print("\n--- Scenario A: Agent vs Agent (Immediate Hingers) ---")
    grid_a = [
        [1, 0, 1],
        [1, 0, 1],
        [1, 1, 1],
    ]
    state_a = State(grid_a, size=3)
    print("Initial board:")
    print(state_a)
    print(f"Number of hingers: {state_a.numHingers()}")
    
    agentA = Agent(size=(3, 3), name="AgentA")
    agentB = Agent(size=(3, 3), name="AgentB")
    
    winner = play(state_a, agentA, agentB)
    print(f"Result: {winner} wins!")
    print(f"Expected: AgentA wins (plays hinger immediately)")
    
    # --- Scenario B: Agent vs Agent (No hingers, mixed values) ---
    print("\n" + "=" * 60)
    print("--- Scenario B: Agent vs Agent (No Hingers, Mixed Values) ---")
    grid_b = [
        [2, 2, 0],
        [2, 2, 2],
        [0, 2, 2],
    ]
    state_b = State(grid_b, size=3)
    print("Initial board:")
    print(state_b)
    print(f"Number of hingers: {state_b.numHingers()}")
    
    agentC = Agent(size=(3, 3), name="AgentC")
    agentD = Agent(size=(3, 3), name="AgentD")
    
    winner = play(state_b, agentC, agentD)
    if winner is None:
        print("Result: Draw (board cleared without hinger)")
    else:
        print(f"Result: {winner} wins!")
    
    # --- Scenario C: Illegal move handling ---
    print("\n" + "=" * 60)
    print("--- Scenario C: Illegal Move Handling ---")
    
    # Create a dummy agent that returns illegal moves
    class DummyAgent:
        def __init__(self, name="Dummy"):
            self.name = name
        
        def move(self, state):
            # Return out-of-bounds move
            return (-1, 99)
    
    grid_c = [
        [1, 1],
        [1, 1],
    ]
    state_c = State(grid_c, size=2)
    print("Initial board:")
    print(state_c)
    
    dummy = DummyAgent(name="BadAgent")
    agentE = Agent(size=(2, 2), name="GoodAgent")
    
    winner = play(state_c, dummy, agentE)
    print(f"Result: {winner} wins!")
    print(f"Expected: GoodAgent wins (BadAgent made illegal move)")
    
    # --- Summary ---
    print("\n" + "=" * 60)
    print("All tests completed.")
    print("=" * 60)
    
    return True


if __name__ == "__main__":
    tester()
