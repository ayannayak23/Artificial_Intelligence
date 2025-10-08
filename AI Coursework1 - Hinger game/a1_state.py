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
    
    def numRegions():
        numRegions = 0
        if self.grid[r]-[r+1] and self.grid[c]-[c+1] = 1:
            numRegions += 1
        return numRegions