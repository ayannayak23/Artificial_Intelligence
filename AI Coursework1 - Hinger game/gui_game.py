# -*- coding: utf-8 -*-
# GUI for Hinger Game using Tkinter
# Supports Human vs Agent (3x3) and Agent vs Agent (5x5) with move counters and timeouts

import tkinter as tk
from tkinter import ttk, messagebox
import time
from dataclasses import dataclass
from typing import Optional, Literal, Tuple

from a1_state import State
from a3_agent import Agent
from stream_core import is_legal, is_hinger_now, apply_move, board_cleared


# UI message constants
MSG_START = "Click Start to begin"
MSG_TO_MOVE = "to move"
MSG_ILLEGAL = "Illegal move by"
MSG_TIMEOUT = "Timeout!"
MSG_HINGER = "HINGER!"
MSG_DRAW = "Draw: board cleared without any hinger played"
MSG_NO_MOVES = "has no legal moves"


@dataclass
class GuiConfig:
    # GUI configuration constants
    cell_size: int = 60  # Pixel size of each board cell
    a_vs_a_delay_ms: int = 1000  # Delay between agent moves (ms)
    human_timeout_seconds: int = 15  # Human turn timeout
    tick_interval_ms: int = 250  # UI refresh rate for timers
    
    def size_for_mode(self, mode: str) -> int:
        # Return board size for game mode (3 for human, 5 for agent vs agent)
        return 3 if mode == "human_vs_agent" else 5


class BoardView:
    # Handles board rendering and coordinate mapping
    
    def __init__(self, canvas: tk.Canvas, cell_size: int):
        self.canvas = canvas
        self.cell_size = cell_size
        
    def draw(self, state: State, size: int):
        # Draw the game board with colored cells and values
        self.canvas.delete("all")
        for r in range(size):
            for c in range(size):
                x0, y0 = c * self.cell_size, r * self.cell_size
                x1, y1 = x0 + self.cell_size, y0 + self.cell_size
                value = state.grid[r][c]
                # Highlight hingers (value=1) with yellow background
                bg = "#ffffcc" if value == 1 else "white"
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=bg, outline="#666", width=2)
                if value > 0:
                    self.canvas.create_text(x0 + self.cell_size // 2, y0 + self.cell_size // 2,
                                           text=str(value), font=("Arial", 20, "bold"), fill="black")
                    
    def pixel_to_cell(self, x: int, y: int) -> Tuple[int, int]:
        # Convert pixel coordinates to grid (row, col)
        return (y // self.cell_size, x // self.cell_size)


class HingerGUI:
    # Tkinter GUI for Hinger game with timing and move counting
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Hinger Game")
        self.cfg = GuiConfig()
        
        # Game state variables
        self.state: Optional[State] = None
        self.agentA: Optional[Agent] = None  # None means human player
        self.agentB: Optional[Agent] = None
        self.current: Literal["A", "B"] = "A"  # Current player
        self.hinger_played = False  # Track if any hinger has been played
        self.game_active = False  # Is game in progress?
        self.move_number = 1  # Move counter
        self.board_size = 3  # Current board size (3 or 5)
        
        # Timing variables
        self.game_start_time = 0.0  # Game start timestamp
        self.human_deadline: Optional[float] = None  # Timeout deadline for human
        self.tick_id: Optional[str] = None  # Timer callback ID
        
        self.setup_ui()
        
    def setup_ui(self):
        # Create all UI elements: control bar, status bar, canvas, message label
        # Control bar (mode selector, agent settings, start/reset buttons)
        ctrl = tk.Frame(self.root, padx=10, pady=10)
        ctrl.pack(side=tk.TOP, fill=tk.X)
        tk.Label(ctrl, text="Mode:").grid(row=0, column=0)
        self.mode_var = tk.StringVar(value="human_vs_agent")
        ttk.Combobox(ctrl, textvariable=self.mode_var, values=["human_vs_agent", "agent_vs_agent"],
                     state="readonly", width=15).grid(row=0, column=1, padx=5)
        tk.Label(ctrl, text="Agent:").grid(row=0, column=2, padx=(20,0))
        self.agent_mode_var = tk.StringVar(value="alphabeta")
        ttk.Combobox(ctrl, textvariable=self.agent_mode_var, values=["alphabeta", "minimax"],
                     state="readonly", width=10).grid(row=0, column=3, padx=5)
        tk.Label(ctrl, text="Depth:").grid(row=0, column=4, padx=(20,0))
        self.depth_var = tk.IntVar(value=3)
        tk.Spinbox(ctrl, from_=2, to=6, textvariable=self.depth_var, width=5).grid(row=0, column=5, padx=5)
        tk.Button(ctrl, text="Start", command=self.start_game, bg="#4CAF50", fg="white", padx=10).grid(row=0, column=6, padx=10)
        tk.Button(ctrl, text="Reset", command=self.reset_game, bg="#f44336", fg="white", padx=10).grid(row=0, column=7, padx=5)
        
        # Status bar (turn, move count, timers)
        status = tk.Frame(self.root, padx=10, pady=5, bg="#e0e0e0")
        status.pack(side=tk.TOP, fill=tk.X)
        self.turn_label = tk.Label(status, text="Turn: —", bg="#e0e0e0", font=("Arial", 10, "bold"))
        self.turn_label.pack(side=tk.LEFT, padx=10)
        self.move_label = tk.Label(status, text="Move #: —", bg="#e0e0e0", font=("Arial", 10))
        self.move_label.pack(side=tk.LEFT, padx=10)
        self.human_time_label = tk.Label(status, text="Human time: —", bg="#e0e0e0", font=("Arial", 10))
        self.human_time_label.pack(side=tk.LEFT, padx=10)
        self.total_time_label = tk.Label(status, text="Total: 0.0s", bg="#e0e0e0", font=("Arial", 10))
        self.total_time_label.pack(side=tk.LEFT, padx=10)
        
        # Canvas for board display (sized for 5x5 max)
        self.canvas = tk.Canvas(self.root, width=self.cfg.cell_size * 5, height=self.cfg.cell_size * 5,
                               bg="white", highlightthickness=1, highlightbackground="#666")
        self.canvas.pack(side=tk.TOP, padx=10, pady=10)
        self.canvas.bind("<Button-1>", self.on_canvas_click)  # Handle mouse clicks
        self.board_view = BoardView(self.canvas, self.cfg.cell_size)
        
        # Status message label
        self.status_text = tk.StringVar(value=MSG_START)
        tk.Label(self.root, textvariable=self.status_text, font=("Arial", 11), fg="#1976D2", pady=10).pack()
        
    def start_game(self):
        # Initialize and start a new game
        self.board_size = self.cfg.size_for_mode(self.mode_var.get())
        # Different starting grids for 3x3 vs 5x5
        grid = [[2,2,0],[2,2,2],[0,2,2]] if self.board_size == 3 else \
               [[2,1,0,1,2],[1,2,1,2,1],[0,1,2,1,0],[1,2,1,2,1],[2,1,0,1,2]]
        self.state = State(grid, size=self.board_size)
        
        # Create agents based on mode
        is_human_mode = self.mode_var.get() == "human_vs_agent"
        self.agentA = None if is_human_mode else Agent((self.board_size, self.board_size), "AgentA")
        self.agentB = Agent((self.board_size, self.board_size), "Bot" if is_human_mode else "AgentB")
        
        # Reset game state
        self.current = "A"
        self.hinger_played = False
        self.game_active = True
        self.move_number = 1
        self.game_start_time = time.monotonic()
        self.human_deadline = None
        
        self.board_view.draw(self.state, self.board_size)
        self.update_labels()
        self.status_text.set(f"{self._player_name()} {MSG_TO_MOVE}")
        
        # Start timer tick
        if self.tick_id:
            self.root.after_cancel(self.tick_id)
        self.tick()
        
        # Start first turn
        if self.agentA:
            # Agent vs Agent: kick off agent turn
            self.root.after(100, self.step_agent_turn)
        else:
            # Human vs Agent: start human timeout
            self.human_deadline = time.monotonic() + self.cfg.human_timeout_seconds
            
    def reset_game(self):
        # Reset to initial state
        if self.tick_id:
            self.root.after_cancel(self.tick_id)
            self.tick_id = None
        self.game_active = False
        self.state = None
        self.human_deadline = None
        self.canvas.delete("all")
        self.status_text.set(MSG_START)
        # Reset all labels to default
        for lbl, txt in [(self.turn_label, "Turn: —"), (self.move_label, "Move #: —"),
                        (self.human_time_label, "Human time: —"), (self.total_time_label, "Total: 0.0s")]:
            lbl.config(text=txt)
            
    def _player_name(self, player: Optional[str] = None) -> str:
        # Get player name (agent name or "Human X")
        p = player or self.current
        agent = self.agentA if p == "A" else self.agentB
        return agent.name if agent else f"Human {p}"
        
    def _opponent_name(self) -> str:
        # Get opponent name
        return self._player_name("B" if self.current == "A" else "A")
        
    def on_canvas_click(self, event):
        # Handle human click on canvas
        if not self.game_active or not self.state:
            return
        agent = self.agentA if self.current == "A" else self.agentB
        if agent:
            return  # Ignore clicks during agent turns
        # Convert pixel coords to grid coords
        r, c = self.board_view.pixel_to_cell(event.x, event.y)
        if 0 <= r < self.board_size and 0 <= c < self.board_size:
            self.perform_turn(r, c, "human")
            
    def step_agent_turn(self):
        # Execute agent move
        if not self.game_active or not self.state:
            return
        agent = self.agentA if self.current == "A" else self.agentB
        if not agent:
            return
        # Get agent's move
        move = agent.move(self.state, mode=self.agent_mode_var.get(), depth=self.depth_var.get())
        if not move:
            # No legal moves: opponent wins
            self.end_game(f"{self._player_name()} {MSG_NO_MOVES}", self._opponent_name())
            return
        r, c = move
        self.perform_turn(r, c, "agent")
        
    def perform_turn(self, r: int, c: int, source: Literal["human", "agent"]):
        # Execute a turn: legality, hinger check, apply, terminal checks, switch
        if not is_legal(self.state, r, c):
            self.end_game(f"{MSG_ILLEGAL} {self._player_name()}", self._opponent_name())
            return
        
        # Check hinger BEFORE applying move
        is_h = is_hinger_now(self.state, r, c)
        apply_move(self.state, r, c)
        self.move_number += 1
        self.board_view.draw(self.state, self.board_size)
        self.update_labels()
        
        # Check for hinger win
        if is_h:
            self.hinger_played = True
            self.end_game(f"{MSG_HINGER} {self._player_name()} wins at ({r},{c})", self._player_name())
            return
        
        # Check for draw (cleared board without hinger)
        if board_cleared(self.state) and not self.hinger_played:
            self.end_game(MSG_DRAW, None)
            return
        
        # Switch player
        self.current = "B" if self.current == "A" else "A"
        self.update_labels()
        self.status_text.set(f"{self._player_name()} {MSG_TO_MOVE}")
        
        # Schedule next turn
        next_agent = self.agentA if self.current == "A" else self.agentB
        if next_agent:
            # Next player is agent: schedule agent turn
            self.root.after(self.cfg.a_vs_a_delay_ms if source == "agent" else 500, self.step_agent_turn)
        else:
            # Next player is human: start timeout
            self.human_deadline = time.monotonic() + self.cfg.human_timeout_seconds
            
    def tick(self):
        # UI heartbeat for timers (called every tick_interval_ms)
        if not self.game_active:
            return
        elapsed = time.monotonic() - self.game_start_time
        self.total_time_label.config(text=f"Total: {elapsed:.1f}s")
        
        # Update human timeout countdown
        agent = self.agentA if self.current == "A" else self.agentB
        if not agent and self.human_deadline:
            remaining = max(0, self.human_deadline - time.monotonic())
            self.human_time_label.config(text=f"Human: {int(remaining)}s")
            if remaining <= 0:
                # Human timeout: opponent wins
                self.end_game(f"{MSG_TIMEOUT} {self._player_name()} took too long", self._opponent_name())
                return
        else:
            self.human_time_label.config(text="Human: —")
        
        # Schedule next tick
        self.tick_id = self.root.after(self.cfg.tick_interval_ms, self.tick)
        
    def update_labels(self):
        # Update turn and move labels
        self.turn_label.config(text=f"Turn: {self.current} ({self._player_name()})")
        self.move_label.config(text=f"Move #: {self.move_number}")
        
    def end_game(self, message: str, winner: Optional[str]):
        # End game and show summary dialog
        self.game_active = False
        self.human_deadline = None
        total_moves = self.move_number - 1
        total_time = time.monotonic() - self.game_start_time
        self.status_text.set(message)
        summary = f"{message}\n\nTotal Moves: {total_moves}\nTotal Time: {total_time:.1f}s"
        messagebox.showinfo("Game Over" + ("" if winner else " - Draw"), summary)
        self.total_time_label.config(text=f"Total: {total_time:.1f}s")


def main():
    # Entry point: create Tkinter window and start event loop
    root = tk.Tk()
    HingerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
