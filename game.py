# -*- coding: utf-8 -*-
"""
Created on Tue Oct 14 11:11:36 2025

@author: ust23chu
"""

from agent import Agent
from state import State

def play(state, agentA, agentB):
    
    turn = 'X'
    
    if(agentA == None):
        while(state.is_terminal() == False):
            if(turn == 'X'):
                input1 = input('Enter your row:')
                row = int(input1)
                input2 = input('Enter your column:')
                column = int(input2)
                state.make_move(row, column, 'X')
                print(state)
                turn = 'O'
            else:
                move = agentB.get_move(state)
                state.make_move(move[0], move[1], agentB.player)
                print(state)
                turn = 'X'
                
    else:
    
        while(state.is_terminal() == False):
            
            if(turn == 'X'):
                move = agentA.get_move(state)
                state.make_move(move[0], move[1], agentA.player)
                print(turn + '\n')
                turn = 'O'
            else:
                move = agentB.get_move(state)
                state.make_move(move[0], move[1], agentB.player)
                print(turn + '\n')
                turn = 'X'
                
    return state.get_winner()
            
            

agentA = Agent('X')
agentB = Agent('O')

state = State([[' ',' ',' '],[' ',' ',' '], [' ',' ',' ']])

    
print(play(state, None, agentB)) 
    


