# -*- coding: utf-8 -*-
"""
Hinger Project
Coursework 001 for: CMP-6058A Artificial Intelligence

Defines the State class for Task 1

@author: B9 (1004411839, 100434969, and 100440712)
@date: 08/10/2025
"""

class State:
    size = 5
    
    # Initialize a State oobject.
    def __init__(self, grid=None, size=5):
        if grid is None:
            self.grid = [[0 for _ in range(size)] for _ in range(size)]
        else:
            self.grid = [row[:] for row in grid]

    # Return a string representation of the grid
    def __str__(self):
        lines = []
        for row in self.grid:
            line = " ".join(str(cell) for cell in row)
            lines.append(line)
        return "\n".join(lines)

    # Generator that yields all possible next states (Calculating by removing one counter from any non-zero cell)
    def moves(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if self.grid[i][j] > 0:
                    new_state = self.clone()
                    new_state.grid[i][j] -= 1
                    yield new_state 
    
    # Create a copy of the current state (current grid)
    def clone(self):
        new_state = State(None)
        new_state.grid = [row[:] for row in self.grid]
        return new_state
    
    # Counts the numner of regions of non-zero cell
    def numRegions(self):
        rows, cols = len(self.grid), len(self.grid[0])
        visited = [[False for _ in range(cols)] for _ in range(rows)]
        regions = 0
    
        # Use DFS to explore connected cells
        def dfs(i, j):
            if i < 0 or i >= rows or j < 0 or j >= cols:
                return
            if visited[i][j] or self.grid[i][j] == 0:
                return
            visited[i][j] = True
            # explore all 8 directions (horizontal, vertical, diagonal)
            for di in [-1, 0, 1]:
                for dj in [-1, 0, 1]:
                    if di != 0 or dj != 0:
                        dfs(i + di, j + dj)
    
        # Counts regions by applying DFS to unvisited non-zero cells
        for i in range(rows):
            for j in range(cols):
                if self.grid[i][j] > 0 and not visited[i][j]:
                    regions += 1
                    dfs(i, j)
    
        return regions

    # Counts the number of hingers (a cell with 1 counter, by removing it increases the number of regions) in the grid
    def numHingers(self):
        count = 0
        current_regions = self.numRegions()
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if self.grid[i][j] == 1:
                    # simulate removing this counter
                    new_state = self.clone()
                    # Change the specific cell to be 0
                    new_state.grid[i][j] = 0
                    # Check if the new_state creates more regions
                    new_regions = new_state.numRegions()
                    if new_regions > current_regions:
                        count += 1
        return count
    
    # Return a list of coordinates of all non-zero cells
    def get_active_cells(self):
        # Return a list of (i, j) coordinates of active (non-zero) cells.
        active = []
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if self.grid[i][j] > 0:
                    active.append((i, j))
        return active
    
    # Check if all cells in the grid are zero by returning True and False
    def is_empty(self):
        # Return True if all cells are empty.
        return all(cell == 0 for row in self.grid for cell in row)

# Function to test the State class and methods
def tester():
    grid = [
        [1, 1, 0, 0, 2],
        [0, 1, 0, 1, 0],
        [1, 0, 0, 0, 0],
        [0, 2, 1, 1, 1],
    ]
    
    test_grid = State(grid)
    
    # Display the grid
    print(test_grid)
    # Number of connected regions
    print("Number of regions:", test_grid.numRegions())
    # Number of hingers
    print("Number of hingers:", test_grid.numHingers())
    # List of active cells
    print("Active cells:", test_grid.get_active_cells())
    # Check if the grid is empty
    print("Is empty?:", test_grid.is_empty())
    
    # Test to find all possible moves
    print("\n=== Possible Moves ===")
    for k, next_state in enumerate(test_grid.moves(), 1):
        print(f"Move {k}:")
        print(next_state)
        print("---")
        
    # Test an empty board
    empty = [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
    ]
    empty_grid = State(empty)
    
    print("\n=== Empty Board ===")
    print(empty_grid)
    print("Is empty?:", empty_grid.is_empty())
    
# Call a tester function only when this file is executed
if __name__ == "__main__":
    tester()


