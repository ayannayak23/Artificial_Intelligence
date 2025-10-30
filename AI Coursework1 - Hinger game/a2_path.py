# -*- coding: utf-8 -*-
"""
Created on Sun Oct 19 15:14:41 2025

@author: Ayan
"""

from collections import deque
import heapq
from a1_state import State

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
            if str(move.grid) not in visited and is_safe_transition(state, move):
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
            if str(move.grid) not in visited and is_safe_transition(state, move):
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
            if str(move.grid) not in visited and is_safe_transition(state, move):
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
def path_astar(start, end):
    def heuristic(s1, s2):
        diff = 0
        for i in range(len(s1.grid)):
            for j in range(len(s1.grid[0])):
                if s1.grid[i][j] != s2.grid[i][j]:
                    diff += 1
        return diff

    open_set = []
    g_score = {str(start.grid): 0}
    counter = 0  # tie-breaker
    heapq.heappush(open_set, (0, counter, start, [start]))

    while open_set:
        _, _, current, path = heapq.heappop(open_set)
        if current.grid == end.grid:
            return path

        for move in current.moves():
            if is_safe_transition(current, move):
                cost = g_score[str(current.grid)] + 1
                if str(move.grid) not in g_score or cost < g_score[str(move.grid)]:
                    g_score[str(move.grid)] = cost
                    f = cost + heuristic(move, end)
                    counter += 1
                    heapq.heappush(open_set, (f, counter, move, path + [move]))
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
 
    
def is_safe_transition(current, next_state):
    """A safe transition avoids hingers and does not increase active regions."""
    if current.numHingers() > 0 or next_state.numHingers() > 0:
        return False
    if next_state.numRegions() > current.numRegions():
        return False
    return True

        
def print_path(path):
    if not path:
        print("No safe path found.\n")
        return
    print("Safe path found (", len(path), "steps):")
    for i, state in enumerate(path):
        print(f"Step {i}:")
        print(state)
        print()
    print("------------------------")


# --- Tester Function ---
def tester():
    print("=== Testing Search Algorithms ===")

    s1 = State([[1, 0, 0, 0, 0],
                [2, 0, 2, 2, 1],
                [2, 0, 0, 0, 2],
                [0, 0, 1, 2, 1]])
    
    s2 = State([[1, 0, 0, 0, 0],
                [2, 0, 2, 2, 1],
                [1, 0, 0, 0, 2],
                [0, 0, 0, 2, 0]])

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

    print("\n--- Compare Algorithms ---")
    compare(s1, s2)


if __name__ == "__main__":
    tester()
