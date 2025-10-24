# -*- coding: utf-8 -*-
"""
Created on Wed Oct  8 04:29:16 2025

@author: User
"""

class State:
    size = 5
    
    def __init__(self, grid=None, size=5):
        if grid is None:
            self.grid = [[0 for _ in range(size)] for _ in range(size)]
        else:
            self.grid = [row[:] for row in grid]

    def __str__(self):
        #Display out the visualization of the grid
        lines = []
        for row in self.grid:
            line = " ".join(str(cell) for cell in row)
            lines.append(line)
        return "\n".join(lines)

    def moves(self):
        #Generator: yields all possible next states (one counter removed).
        for r in range(len(self.grid)):
            for c in range(len(self.grid[0])):
                if self.grid[r][c] > 0:
                    new_state = self.clone()
                    new_state.grid[r][c] -= 1
                    yield new_state 
    
    def clone(self):
        new_state = State(None)
        new_state.grid = [row[:] for row in self.grid]
        return new_state
    
    def numRegions(self):
        rows, cols = len(self.grid), len(self.grid[0])
        visited = [[False for _ in range(cols)] for _ in range(rows)]
        regions = 0
    
        # Helper function for DFS
        def dfs(r, c):
            if r < 0 or r >= rows or c < 0 or c >= cols:
                return
            if visited[r][c] or self.grid[r][c] == 0:
                return
            visited[r][c] = True
            # explore all 8 directions (horizontal, vertical, diagonal)
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr != 0 or dc != 0:
                        dfs(r + dr, c + dc)
    
        # main loop to count connected components
        for r in range(rows):
            for c in range(cols):
                if self.grid[r][c] > 0 and not visited[r][c]:
                    regions += 1
                    dfs(r, c)
    
        return regions

    def numHingers(self):
        count = 0
        current_regions = self.numRegions()
        for r in range(len(self.grid)):
            for c in range(len(self.grid[0])):
                if self.grid[r][c] == 1:
                    # simulate removing this counter
                    new_state = self.clone()
                    #Change the specific cell to be 0
                    new_state.grid[r][c] = 0
                    
                    #Check if the new_state creates more regions or not (if yes, it is hinger)
                    new_regions = new_state.numRegions()
                        
                    # if removing this increases the number of regions
                    if new_regions > current_regions:
                        count += 1
        return count
            