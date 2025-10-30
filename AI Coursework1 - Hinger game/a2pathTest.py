# -*- coding: utf-8 -*-
"""
Created on Sun Oct 19 15:14:41 2025

@author: Ayan
"""

from collections import deque
import heapq
from a1_state import State


# Helper function to check if a move is a hinger move
# A safe path must not include any hinger moves (moves where removing a
# cell with value=1 increases the number of regions)
def _is_hinger_move(state_before, state_after):
    # A hinger move is one where a cell with value=1 is removed
    # AND it increases the number of regions
    regions_before = state_before.numRegions()
    regions_after = state_after.numRegions()
    
    # Find which cell was removed (decreased)
    for r in range(len(state_before.grid)):
        for c in range(len(state_before.grid[0])):
            if state_before.grid[r][c] > state_after.grid[r][c]:
                # This cell was removed/decreased
                # Check if it was a hinger: value was 1 AND regions increased
                if state_before.grid[r][c] == 1 and regions_after > regions_before:
                    return True
    return False

# --- (BFS) ---
def path_BFS(start, end):
    visited = set()
    queue = deque([(start, [start])])
    
    while queue:
        state, path = queue.popleft()
        if state.grid == end.grid:
            return path
        
        visited.add(str(state.grid))
        for move in state.moves():
            # Check: resulting state has no hingers AND the move to get there wasn't a hinger
            if str(move.grid) not in visited and move.numHingers() == 0 and not _is_hinger_move(state, move):
                queue.append((move, path + [move]))
    return None


# --- (DFS) ---
def path_DFS(start, end):
    visited = set()
    stack = [(start, [start])]

    while stack:
        state, path = stack.pop()
        if state.grid == end.grid:
            return path
        
        visited.add(str(state.grid))
        for move in state.moves():
            # Check: resulting state has no hingers AND the move to get there wasn't a hinger
            if str(move.grid) not in visited and move.numHingers() == 0 and not _is_hinger_move(state, move):
                stack.append((move, path + [move]))
    return None


# --- (ID-DFS) ---
def path_IDDFS(start, end, max_depth=10):
    def dfs_limit(state, end, path, depth, visited):
        if depth == 0:
            return None
        if state.grid == end.grid:
            return path
        visited.add(str(state.grid))
        for move in state.moves():
            # Check: resulting state has no hingers AND the move to get there wasn't a hinger
            if str(move.grid) not in visited and move.numHingers() == 0 and not _is_hinger_move(state, move):
                result = dfs_limit(move, end, path + [move], depth - 1, visited)
                if result:
                    return result
        return None

    for limit in range(1, max_depth + 1):
        result = dfs_limit(start, end, [start], limit, set())
        if result:
            return result
    return None


# --- A* Search ---
# Heuristic: Number of cells that differ between current and goal state
# This is admissible (never overestimates) since each move changes at least one cell
def path_astar(start, end):
    def heuristic(s1, s2):
        diff = 0
        for i in range(len(s1.grid)):
            for j in range(len(s1.grid[0])):
                if s1.grid[i][j] != s2.grid[i][j]:
                    diff += 1
        return diff

    open_set = []
    counter = 0  # Tie-breaker for heap when f-scores are equal
    heapq.heappush(open_set, (0, counter, start, [start]))
    g_score = {str(start.grid): 0}

    while open_set:
        _, _, current, path = heapq.heappop(open_set)
        if current.grid == end.grid:
            return path

        for move in current.moves():
            # Check: resulting state has no hingers AND the move to get there wasn't a hinger
            if move.numHingers() == 0 and not _is_hinger_move(current, move):
                cost = g_score[str(current.grid)] + 1
                if str(move.grid) not in g_score or cost < g_score[str(move.grid)]:
                    g_score[str(move.grid)] = cost
                    f = cost + heuristic(move, end)
                    counter += 1
                    heapq.heappush(open_set, (f, counter, move, path + [move]))
    return None


# --- Minimum Cost Safe Path (Uniform Cost Search) ---
# This function finds the safe path with minimal total cost between two states.
# Algorithm choice: Uniform Cost Search (UCS) / Dijkstra's algorithm
# Justification:
#   - UCS explores paths in order of increasing cost, guaranteeing the first
#     solution found is optimal (lowest total cost)
#   - Unlike BFS (assumes unit cost), UCS handles varying move costs correctly
#   - Unlike A* (needs a heuristic), UCS is simpler and always finds optimal
#     solution without needing domain-specific heuristics
#   - Time complexity: O(b^d) where b is branching factor, d is solution depth
#   - Space complexity: O(b^d) for storing frontier
# Move cost: For Hinger game, cost of removing a cell = value of that cell
def min_safe(start, end):
    # Priority queue: (total_cost, counter, state, path)
    # Counter prevents comparison of State objects when costs are equal
    open_set = []
    counter = 0
    heapq.heappush(open_set, (0, counter, start, [(start, 0)]))
    
    # Track best cost to reach each state (for pruning)
    best_cost = {str(start.grid): 0}
    
    while open_set:
        current_cost, _, current, path = heapq.heappop(open_set)
        
        # Goal check
        if current.grid == end.grid:
            # Return path as list of states (without costs)
            return [state for state, _ in path]
        
        # Explore neighbors
        for move in current.moves():
            # Safety check: only consider moves with no hingers AND the move itself isn't a hinger
            if move.numHingers() == 0 and not _is_hinger_move(current, move):
                # Calculate move cost: sum of all values that decreased
                # (In Hinger, each move removes one cell, so cost = cell value)
                move_cost = 0
                for r in range(len(current.grid)):
                    for c in range(len(current.grid[0])):
                        if current.grid[r][c] > move.grid[r][c]:
                            move_cost += current.grid[r][c] - move.grid[r][c]
                
                new_cost = current_cost + move_cost
                state_key = str(move.grid)
                
                # Only explore if this path is cheaper than previously found
                if state_key not in best_cost or new_cost < best_cost[state_key]:
                    best_cost[state_key] = new_cost
                    counter += 1
                    heapq.heappush(open_set, (new_cost, counter, move, path + [(move, move_cost)]))
    
    return None


# --- Compare Algorithms ---
def compare(start, end):
    import time
    algos = [("BFS", path_BFS), ("DFS", path_DFS), ("IDDFS", path_IDDFS), ("A*", path_astar)]
    for name, func in algos:
        start_time = time.time()
        result = func(start, end)
        duration = time.time() - start_time
        print(f"{name:6} | Found: {result is not None} | Steps: {len(result) if result else 0} | Time: {duration:.4f}s")
        
        
def print_path(path):
    if not path:
        print("No safe path found.\n")
        return
    print("Safe path found (", len(path), "steps):")
    for i, state in enumerate(path):
        print(f"Step {i}:")
        print(state)
        print()
    print("-" * 25)


# --- Tester Function ---
def tester():
    print("=== Testing Search Algorithms ===")

    s1 = State([[1, 1], [0, 1]])
    s2 = State([[1, 0], [0, 1]])

    print("Start:\n", s1)
    print("End:\n", s2)

    print("\n--- BFS ---")
    print_path(path_BFS(s1, s2))

    print("\n--- DFS ---")
    print_path(path_DFS(s1, s2))

    print("\n--- IDDFS ---")
    print_path(path_IDDFS(s1, s2))

    print("\n--- A* ---")
    print_path(path_astar(s1, s2))
    
    # Test min_safe with non-binary states (varying costs)
    print("\n=== Testing Minimum Cost Path (min_safe) ===")
    s3 = State([[2, 3, 0], [1, 2, 2], [0, 1, 2]])
    s4 = State([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    
    print("Start (with varying costs):\n", s3)
    print("End (cleared board):\n", s4)
    print("\n--- min_safe (Uniform Cost Search) ---")
    result = min_safe(s3, s4)
    if result:
        print_path(result)
        # Calculate total cost
        total_cost = 0
        for i in range(len(result) - 1):
            for r in range(len(result[i].grid)):
                for c in range(len(result[i].grid[0])):
                    if result[i].grid[r][c] > result[i+1].grid[r][c]:
                        total_cost += result[i].grid[r][c] - result[i+1].grid[r][c]
        print(f"Total path cost: {total_cost}")
    else:
        print("No safe path found.\n")

    # print("\n--- Compare Algorithms ---")
    # compare(s1, s2)


if __name__ == "__main__":
    tester()
