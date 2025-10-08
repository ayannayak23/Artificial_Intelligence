# -*- coding: utf-8 -*-
"""
Created on Wed Oct  8 04:56:52 2025

@author: User
"""

from a1_state import State

grid = [
    [1, 1, 0, 0, 2],
    [0, 1, 0, 1, 0],
    [1, 0, 0, 0, 0],
    [0, 2, 1, 1, 1],
]

state = State(grid)
print(state.__str__())

print("\nPossible next states:\n")
for next_state in state.moves():
    print(next_state, '\n')
    
print(state.numRegions())
print(state.numHingers())