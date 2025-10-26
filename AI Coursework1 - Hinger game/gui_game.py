# -*- coding: utf-8 -*-
"""
GUI for Hinger Game using Tkinter
Supports Human vs Agent (3x3) and Agent vs Agent (5x5) with move counters and timeouts.

@author: Ahmed
"""

import tkinter as tk
from tkinter import ttk, messagebox
import time
from typing import Optional, Literal

from a1_state import State
from a3_agent import Agent
from stream_core import is_legal, is_hinger_now, apply_move, board_cleared


class HingerGUI:
    """Tkinter GUI for Hinger game with timing and move counting."""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Hinger Game")
        
        # Game state
        self.state: Optional[State] = None
        self.agentA: Optional[Agent] = None
        self.agentB: Optional[Agent] = None
        self.current: Literal["A", "B"] = "A"
        self.hinger_played: bool = False
        self.game_active: bool = False
        
        # Move counting
        self.move_number: int = 1
        
        # Timing
        self.game_start_time: float = 0.0
        self.human_deadline: Optional[float] = None
        self.tick_id: Optional[str] = None
        
        # Configuration
        self.cell_size: int = 60
        self.a_vs_a_delay_ms: int = 2000
        self.human_timeout_seconds: int = 15
        self.board_size: int = 3
        
        # UI components
        self.setup_ui()
        
    def setup_ui(self):
        """Create all UI elements."""
        # Top control bar
        control_frame = tk.Frame(self.root, padx=10, pady=10)
        control_frame.pack(side=tk.TOP, fill=tk.X)
        
        # Game mode selection
        tk.Label(control_frame, text="Game Mode:").grid(row=0, column=0, sticky=tk.W)
        self.mode_var = tk.StringVar(value="human_vs_agent")
        mode_combo = ttk.Combobox(control_frame, textvariable=self.mode_var, 
                                   values=["human_vs_agent", "agent_vs_agent"],
                                   state="readonly", width=15)
        mode_combo.grid(row=0, column=1, padx=5)
        mode_combo.bind("<<ComboboxSelected>>", self.on_mode_change)
        
        # Agent mode selection
        tk.Label(control_frame, text="Agent Mode:").grid(row=0, column=2, padx=(20,0), sticky=tk.W)
        self.agent_mode_var = tk.StringVar(value="alphabeta")
        agent_mode_combo = ttk.Combobox(control_frame, textvariable=self.agent_mode_var,
                                        values=["alphabeta", "minimax"],
                                        state="readonly", width=10)
        agent_mode_combo.grid(row=0, column=3, padx=5)
        
        # Depth selection
        tk.Label(control_frame, text="Depth:").grid(row=0, column=4, padx=(20,0), sticky=tk.W)
        self.depth_var = tk.IntVar(value=3)
        depth_spin = tk.Spinbox(control_frame, from_=2, to=6, textvariable=self.depth_var,
                                width=5)
        depth_spin.grid(row=0, column=5, padx=5)
        
        # Control buttons
        tk.Button(control_frame, text="Start", command=self.start_game,
                 bg="#4CAF50", fg="white", padx=10).grid(row=0, column=6, padx=10)
        tk.Button(control_frame, text="Reset", command=self.reset_game,
                 bg="#f44336", fg="white", padx=10).grid(row=0, column=7, padx=5)
        
        # Status bar (turn, move#, timers)
        status_frame = tk.Frame(self.root, padx=10, pady=5, bg="#e0e0e0")
        status_frame.pack(side=tk.TOP, fill=tk.X)
        
        self.turn_label = tk.Label(status_frame, text="Turn: —", bg="#e0e0e0", font=("Arial", 10, "bold"))
        self.turn_label.pack(side=tk.LEFT, padx=10)
        
        self.move_label = tk.Label(status_frame, text="Move #: —", bg="#e0e0e0", font=("Arial", 10))
        self.move_label.pack(side=tk.LEFT, padx=10)
        
        self.human_time_label = tk.Label(status_frame, text="Human time: —", bg="#e0e0e0", font=("Arial", 10))
        self.human_time_label.pack(side=tk.LEFT, padx=10)
        
        self.total_time_label = tk.Label(status_frame, text="Total time: 0.0s", bg="#e0e0e0", font=("Arial", 10))
        self.total_time_label.pack(side=tk.LEFT, padx=10)
        
        # Canvas for board
        canvas_size = self.cell_size * 5  # Max size for 5x5
        self.canvas = tk.Canvas(self.root, width=canvas_size, height=canvas_size,
                               bg="white", highlightthickness=1, highlightbackground="#666")
        self.canvas.pack(side=tk.TOP, padx=10, pady=10)
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        
        # Status message
        self.status_text = tk.StringVar(value="Click Start to begin")
        status_msg = tk.Label(self.root, textvariable=self.status_text,
                             font=("Arial", 11), fg="#1976D2", pady=10)
        status_msg.pack(side=tk.TOP)
        
    def on_mode_change(self, event=None):
        """Handle game mode change to adjust board size."""
        mode = self.mode_var.get()
        if mode == "human_vs_agent":
            self.board_size = 3
        else:  # agent_vs_agent
            self.board_size = 5
            
    def start_game(self):
        """Initialize and start a new game."""
        self.on_mode_change()  # Update board size
        
        # Create initial grid
        if self.board_size == 3:
            grid = [
                [2, 2, 0],
                [2, 2, 2],
                [0, 2, 2],
            ]
        else:  # 5x5
            grid = [
                [2, 1, 0, 1, 2],
                [1, 2, 1, 2, 1],
                [0, 1, 2, 1, 0],
                [1, 2, 1, 2, 1],
                [2, 1, 0, 1, 2],
            ]
        
        self.state = State(grid, size=self.board_size)
        
        # Create agents based on mode
        mode = self.mode_var.get()
        if mode == "human_vs_agent":
            self.agentA = None  # Human
            self.agentB = Agent(size=(self.board_size, self.board_size), name="Bot")
        else:  # agent_vs_agent
            self.agentA = Agent(size=(self.board_size, self.board_size), name="AgentA")
            self.agentB = Agent(size=(self.board_size, self.board_size), name="AgentB")
        
        # Reset game state
        self.current = "A"
        self.hinger_played = False
        self.game_active = True
        self.move_number = 1
        self.game_start_time = time.monotonic()
        self.human_deadline = None
        
        # Draw board and update UI
        self.draw_board()
        self.update_labels()
        self.status_text.set(f"{self.get_current_player_name()} to move")
        
        # Start tick timer
        if self.tick_id:
            self.root.after_cancel(self.tick_id)
        self.tick()
        
        # If first player is agent, schedule their move
        if self.agentA is not None:
            self.root.after(100, self.step_agent_turn)
        else:
            # Human starts - set timeout
            self.human_deadline = time.monotonic() + self.human_timeout_seconds
            
    def reset_game(self):
        """Reset the game to initial state."""
        if self.tick_id:
            self.root.after_cancel(self.tick_id)
            self.tick_id = None
        
        self.game_active = False
        self.state = None
        self.current = "A"
        self.hinger_played = False
        self.move_number = 1
        self.human_deadline = None
        
        self.canvas.delete("all")
        self.status_text.set("Click Start to begin")
        self.turn_label.config(text="Turn: —")
        self.move_label.config(text="Move #: —")
        self.human_time_label.config(text="Human time: —")
        self.total_time_label.config(text="Total time: 0.0s")
        
    def get_current_player_name(self) -> str:
        """Get the name of the current player."""
        if self.current == "A":
            return self.agentA.name if self.agentA else "Human A"
        else:
            return self.agentB.name if self.agentB else "Human B"
            
    def get_opponent_name(self) -> str:
        """Get the name of the opponent."""
        opp = "B" if self.current == "A" else "A"
        if opp == "A":
            return self.agentA.name if self.agentA else "Human A"
        else:
            return self.agentB.name if self.agentB else "Human B"
            
    def on_canvas_click(self, event):
        """Handle human click on canvas."""
        if not self.game_active or self.state is None:
            return
        
        # Check if it's a human's turn
        current_agent = self.agentA if self.current == "A" else self.agentB
        if current_agent is not None:
            return  # Agent's turn, ignore clicks
        
        # Map click to grid coordinates
        r = event.y // self.cell_size
        c = event.x // self.cell_size
        
        # Validate bounds
        if r < 0 or r >= self.board_size or c < 0 or c >= self.board_size:
            return
        
        # Check legality
        if not is_legal(self.state, r, c):
            self.end_game(f"Illegal move by {self.get_current_player_name()}",
                         winner=self.get_opponent_name())
            return
        
        # Check for hinger BEFORE applying
        is_h = is_hinger_now(self.state, r, c)
        
        # Apply move
        apply_move(self.state, r, c)
        self.move_number += 1
        
        # Redraw and update
        self.draw_board()
        self.update_labels()
        
        # Check terminal conditions
        if is_h:
            self.hinger_played = True
            self.end_game(f"HINGER! {self.get_current_player_name()} wins by playing hinger at ({r},{c})",
                         winner=self.get_current_player_name())
            return
        
        if board_cleared(self.state) and not self.hinger_played:
            self.end_game("Draw: board cleared without any hinger played", winner=None)
            return
        
        # Switch player
        self.current = "B" if self.current == "A" else "A"
        self.update_labels()
        self.status_text.set(f"{self.get_current_player_name()} to move")
        
        # Check if next player is agent
        next_agent = self.agentA if self.current == "A" else self.agentB
        if next_agent is not None:
            self.root.after(500, self.step_agent_turn)
        else:
            # Next is human - reset timeout
            self.human_deadline = time.monotonic() + self.human_timeout_seconds
            
    def step_agent_turn(self):
        """Execute one agent move."""
        if not self.game_active or self.state is None:
            return
        
        current_agent = self.agentA if self.current == "A" else self.agentB
        if current_agent is None:
            return  # Should not happen
        
        # Get agent's move
        mode = self.agent_mode_var.get()
        depth = self.depth_var.get()
        
        move = current_agent.move(self.state, mode=mode, depth=depth)
        
        if move is None:
            self.end_game(f"{self.get_current_player_name()} has no legal moves",
                         winner=self.get_opponent_name())
            return
        
        r, c = move
        
        # Check legality (should always be legal from agent)
        if not is_legal(self.state, r, c):
            self.end_game(f"Illegal move by {self.get_current_player_name()}",
                         winner=self.get_opponent_name())
            return
        
        # Check for hinger BEFORE applying
        is_h = is_hinger_now(self.state, r, c)
        
        # Apply move
        apply_move(self.state, r, c)
        self.move_number += 1
        
        # Redraw and update
        self.draw_board()
        self.update_labels()
        
        # Check terminal conditions
        if is_h:
            self.hinger_played = True
            self.end_game(f"HINGER! {self.get_current_player_name()} wins by playing hinger at ({r},{c})",
                         winner=self.get_current_player_name())
            return
        
        if board_cleared(self.state) and not self.hinger_played:
            self.end_game("Draw: board cleared without any hinger played", winner=None)
            return
        
        # Switch player
        self.current = "B" if self.current == "A" else "A"
        self.update_labels()
        self.status_text.set(f"{self.get_current_player_name()} to move")
        
        # Schedule next move
        next_agent = self.agentA if self.current == "A" else self.agentB
        if next_agent is not None:
            # Agent vs Agent - delay between moves
            self.root.after(self.a_vs_a_delay_ms, self.step_agent_turn)
        else:
            # Next is human - set timeout
            self.human_deadline = time.monotonic() + self.human_timeout_seconds
            
    def tick(self):
        """UI heartbeat for updating timers."""
        if not self.game_active:
            return
        
        # Update total elapsed time
        elapsed = time.monotonic() - self.game_start_time
        self.total_time_label.config(text=f"Total time: {elapsed:.1f}s")
        
        # Update human timeout if applicable
        current_agent = self.agentA if self.current == "A" else self.agentB
        if current_agent is None and self.human_deadline is not None:
            remaining = max(0, self.human_deadline - time.monotonic())
            self.human_time_label.config(text=f"Human time: {int(remaining)}s")
            
            if remaining <= 0:
                self.end_game(f"Timeout! {self.get_current_player_name()} took too long",
                             winner=self.get_opponent_name())
                return
        else:
            self.human_time_label.config(text="Human time: —")
        
        # Reschedule tick
        self.tick_id = self.root.after(250, self.tick)
        
    def draw_board(self):
        """Draw the game board on canvas."""
        self.canvas.delete("all")
        
        if self.state is None:
            return
        
        for r in range(self.board_size):
            for c in range(self.board_size):
                x0 = c * self.cell_size
                y0 = r * self.cell_size
                x1 = x0 + self.cell_size
                y1 = y0 + self.cell_size
                
                value = self.state.grid[r][c]
                
                # Background color (slight tint for value==1)
                bg_color = "#ffffcc" if value == 1 else "white"
                
                self.canvas.create_rectangle(x0, y0, x1, y1,
                                            fill=bg_color, outline="#666", width=2)
                
                # Draw cell value
                if value > 0:
                    self.canvas.create_text(x0 + self.cell_size // 2,
                                          y0 + self.cell_size // 2,
                                          text=str(value),
                                          font=("Arial", 20, "bold"),
                                          fill="black")
                    
    def update_labels(self):
        """Update status labels."""
        self.turn_label.config(text=f"Turn: {self.current} ({self.get_current_player_name()})")
        self.move_label.config(text=f"Move #: {self.move_number}")
        
    def end_game(self, message: str, winner: Optional[str]):
        """End the game and show summary."""
        self.game_active = False
        self.human_deadline = None
        
        total_moves = self.move_number - 1
        total_time = time.monotonic() - self.game_start_time
        
        self.status_text.set(message)
        
        # Show summary dialog
        summary = f"{message}\n\n"
        summary += f"Total Moves: {total_moves}\n"
        summary += f"Total Time: {total_time:.1f}s"
        
        if winner:
            messagebox.showinfo("Game Over", summary)
        else:
            messagebox.showinfo("Game Over - Draw", summary)
            
        # Update final labels
        self.total_time_label.config(text=f"Total time: {total_time:.1f}s")


def main():
    """Entry point for GUI."""
    root = tk.Tk()
    app = HingerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
