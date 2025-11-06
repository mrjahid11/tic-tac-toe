import tkinter as tk
from tkinter import messagebox
import random


class TicTacToeApp:
    def __init__(self, root=None):
        self.root = root or tk.Tk()
        self.root.title("Tic Tac Toe — Play with Friends")
        self.root.resizable(False, False)

        # Game state
        self.board = [None] * 9  # 'X', 'O', or None
        self.current = 'X'
        self.scores = {'X': 0, 'O': 0}
        self.buttons = [None] * 9

        # Mode: '2P' or 'Single' (human is X, AI is O)
        self.mode = tk.StringVar(value='2P')
        self.difficulty = tk.StringVar(value='Hard')
        # human choice variable (X or O) - default X
        self.human_choice = tk.StringVar(value='X')
        self.human_symbol = 'X'
        self.ai_symbol = 'O'

        # Modern color palette
        self.bg_main = '#1a1a2e'  # dark blue-gray
        self.bg_secondary = '#16213e'  # darker shade
        self.accent_primary = '#0f3460'  # blue accent
        self.accent_highlight = '#e94560'  # red/pink accent
        self.text_light = '#eaeaea'
        self.text_dark = '#1a1a2e'
        self.btn_bg = '#ffffff'
        self.btn_hover = '#f0f0f0'
        self.x_color = '#4ecdc4'  # teal for X
        self.o_color = '#ff6b6b'  # coral for O
        
        self.root.configure(bg=self.bg_main)
        self.btn_font = ("Arial", 28, "bold")
        self.heading_font = ("Arial", 16, "bold")
        self.info_font = ("Arial", 11)

        # Title section
        title_frame = tk.Frame(self.root, bg=self.bg_main, pady=20)
        title_frame.grid(row=0, column=0, sticky='ew')
        
        title = tk.Label(title_frame, text="TIC TAC TOE", font=("Arial", 24, "bold"), 
                        bg=self.bg_main, fg=self.text_light)
        title.pack()
        
        # Turn indicator (prominent display)
        self.turn_label = tk.Label(title_frame, text="X's Turn", font=self.heading_font, 
                                   bg=self.bg_main, fg=self.x_color, pady=8)
        self.turn_label.pack()

        # Controls section
        controls_frame = tk.Frame(self.root, bg=self.bg_secondary, padx=20, pady=15)
        controls_frame.grid(row=1, column=0, sticky='ew')

        # Left controls
        left_controls = tk.Frame(controls_frame, bg=self.bg_secondary)
        left_controls.pack(side='left')
        
        # Mode selection
        tk.Label(left_controls, text="Mode:", font=self.info_font, bg=self.bg_secondary, fg=self.text_light).pack(side='left', padx=(0, 5))
        tk.Radiobutton(left_controls, text="2 Players", variable=self.mode, value='2P', 
                      bg=self.bg_secondary, fg=self.text_light, selectcolor=self.accent_primary,
                      activebackground=self.bg_secondary, activeforeground=self.text_light,
                      font=self.info_font, command=self._mode_changed).pack(side='left', padx=3)
        tk.Radiobutton(left_controls, text="vs AI", variable=self.mode, value='Single', 
                      bg=self.bg_secondary, fg=self.text_light, selectcolor=self.accent_primary,
                      activebackground=self.bg_secondary, activeforeground=self.text_light,
                      font=self.info_font, command=self._mode_changed).pack(side='left', padx=3)

        # Difficulty
        tk.Label(left_controls, text="│", font=self.info_font, bg=self.bg_secondary, fg=self.accent_primary).pack(side='left', padx=8)
        tk.Label(left_controls, text="Difficulty:", font=self.info_font, bg=self.bg_secondary, fg=self.text_light).pack(side='left', padx=(0, 5))
        diff_menu = tk.OptionMenu(left_controls, self.difficulty, 'Easy', 'Hard')
        diff_menu.config(bg=self.accent_primary, fg=self.text_light, font=self.info_font, 
                        highlightthickness=0, bd=0, activebackground=self.accent_highlight)
        diff_menu["menu"].config(bg=self.accent_primary, fg=self.text_light, font=self.info_font)
        diff_menu.pack(side='left', padx=3)

        # Human symbol choice
        tk.Label(left_controls, text="│", font=self.info_font, bg=self.bg_secondary, fg=self.accent_primary).pack(side='left', padx=8)
        tk.Label(left_controls, text="You play:", font=self.info_font, bg=self.bg_secondary, fg=self.text_light).pack(side='left', padx=(0, 5))
        tk.Radiobutton(left_controls, text='X', variable=self.human_choice, value='X', 
                      bg=self.bg_secondary, fg=self.x_color, selectcolor=self.accent_primary,
                      activebackground=self.bg_secondary, activeforeground=self.x_color,
                      font=("Arial", 11, "bold"), command=self._human_symbol_changed).pack(side='left', padx=2)
        tk.Radiobutton(left_controls, text='O', variable=self.human_choice, value='O', 
                      bg=self.bg_secondary, fg=self.o_color, selectcolor=self.accent_primary,
                      activebackground=self.bg_secondary, activeforeground=self.o_color,
                      font=("Arial", 11, "bold"), command=self._human_symbol_changed).pack(side='left', padx=2)

        # Right side - scores
        score_frame = tk.Frame(controls_frame, bg=self.bg_secondary)
        score_frame.pack(side='right')
        
        tk.Label(score_frame, text="SCORE", font=("Arial", 10, "bold"), 
                bg=self.bg_secondary, fg=self.text_light).pack()
        score_display = tk.Frame(score_frame, bg=self.bg_secondary)
        score_display.pack()
        self.score_x = tk.Label(score_display, text=f"X: {self.scores['X']}", font=("Arial", 13, "bold"), 
                               bg=self.bg_secondary, fg=self.x_color, padx=8)
        self.score_x.pack(side='left')
        tk.Label(score_display, text="vs", font=self.info_font, bg=self.bg_secondary, fg=self.text_light).pack(side='left', padx=3)
        self.score_o = tk.Label(score_display, text=f"O: {self.scores['O']}", font=("Arial", 13, "bold"), 
                               bg=self.bg_secondary, fg=self.o_color, padx=8)
        self.score_o.pack(side='left')

        # Game board section
        board_frame = tk.Frame(self.root, bg=self.bg_main, padx=30, pady=25)
        board_frame.grid(row=2, column=0)

        for i in range(9):
            btn = tk.Button(board_frame, text="", width=5, height=2, font=self.btn_font,
                            bg=self.btn_bg, fg=self.text_dark, relief='flat', bd=0,
                            cursor='hand2', command=lambda idx=i: self.on_click(idx))
            btn.grid(row=i // 3, column=i % 3, padx=8, pady=8, ipadx=10, ipady=10)
            # Modern hover effect
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=self.btn_hover) if b['state'] != 'disabled' else None)
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg=self.btn_bg) if b['state'] != 'disabled' else None)
            self.buttons[i] = btn

        # Action buttons at bottom
        bottom_frame = tk.Frame(self.root, bg=self.bg_main, pady=15)
        bottom_frame.grid(row=3, column=0)

        # Styled action buttons
        rematch_btn = tk.Button(bottom_frame, text="↻ rematch", font=("Arial", 11, "bold"), 
                               bg=self.accent_primary, fg=self.text_light, relief='flat', bd=0,
                               padx=20, pady=8, cursor='hand2', command=self.rematch)
        rematch_btn.pack(side='left', padx=6)
        rematch_btn.bind("<Enter>", lambda e: rematch_btn.configure(bg=self.accent_highlight))
        rematch_btn.bind("<Leave>", lambda e: rematch_btn.configure(bg=self.accent_primary))

        new_btn = tk.Button(bottom_frame, text="⟳ New Game", font=("Arial", 11, "bold"),
                           bg=self.accent_primary, fg=self.text_light, relief='flat', bd=0,
                           padx=20, pady=8, cursor='hand2', command=self.new_game)
        new_btn.pack(side='left', padx=6)
        new_btn.bind("<Enter>", lambda e: new_btn.configure(bg=self.accent_highlight))
        new_btn.bind("<Leave>", lambda e: new_btn.configure(bg=self.accent_primary))

        quit_btn = tk.Button(bottom_frame, text="✕ Quit", font=("Arial", 11, "bold"),
                            bg=self.bg_secondary, fg=self.text_light, relief='flat', bd=0,
                            padx=20, pady=8, cursor='hand2', command=self.root.destroy)
        quit_btn.pack(side='left', padx=6)
        quit_btn.bind("<Enter>", lambda e: quit_btn.configure(bg=self.accent_highlight))
        quit_btn.bind("<Leave>", lambda e: quit_btn.configure(bg=self.bg_secondary))

    def on_click(self, idx: int):
        if self.board[idx] is not None:
            return 
        
        self.board[idx] = self.current
        btn = self.buttons[idx]
        # Color X and O differently
        color = self.x_color if self.current == 'X' else self.o_color
        btn.config(text=self.current, state='disabled', disabledforeground=color, bg='#e8e8e8')

        winner, combo = self.check_winner()
        if winner:
            self.scores[winner] += 1
            self.update_scores()
            self.highlight_win(combo)
            messagebox.showinfo("We have a winner", f"{winner} wins!")
            self.disable_board()
            return

        if all(v is not None for v in self.board):
            messagebox.showinfo("Draw", "It's a !")
            return

        self.current = 'O' if self.current == 'X' else 'X'
        # Update turn label with color
        turn_color = self.x_color if self.current == 'X' else self.o_color
        self.turn_label.config(text=f"{self.current}'s Turn", fg=turn_color)

        # If single-player and it's AI's turn, make AI move after a short delay
        if self.mode.get() == 'Single' and self.current == self.ai_symbol:
            self.root.after(250, self.ai_move)

    def check_winner(self):
        wins = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)
        ]
        for a, b, c in wins:
            if self.board[a] and self.board[a] == self.board[b] == self.board[c]:
                return self.board[a], (a, b, c)
        return None, None

    def highlight_win(self, combo):
        # Flash winning buttons with accent color
        flashes = 6
        def _flash(i=0):
            color = self.accent_highlight if i % 2 == 0 else '#ffd93d'
            for idx in combo:
                self.buttons[idx].configure(bg=color)
            if i < flashes:
                self.root.after(150, lambda: _flash(i+1))
        _flash(0)

    def disable_board(self):
        for btn in self.buttons:
            btn.configure(state='disabled')

    def rematch(self):
        # Clear board but keep scores
        self.board = [None] * 9
        for btn in self.buttons:
            btn.configure(text='', state='normal', bg=self.btn_bg)
        self.current = 'X'
        self.turn_label.config(text="X's Turn", fg=self.x_color)
        # If single-player and AI starts (human picked O), schedule AI move
        if self.mode.get() == 'Single' and self.ai_symbol == 'X':
            self.root.after(300, self.ai_move)

    def new_game(self):
        # Reset both board and scores
        self.scores = {'X': 0, 'O': 0}
        self.update_scores()
        self.rematch()

    # --- Mode / AI logic ---
    def _mode_changed(self):
        # When changing mode, rematch the board (keep scores)
        self.rematch()

    def _human_symbol_changed(self):
        # update symbols and rematch so correct player begins
        self.human_symbol = self.human_choice.get()
        self.ai_symbol = 'O' if self.human_symbol == 'X' else 'X'
        self.rematch()

    def ai_move(self):
        # pick a move depending on difficulty
        available = [i for i, v in enumerate(self.board) if v is None]
        if not available:
            return

        if self.difficulty.get() == 'Easy':
            choice = random.choice(available)
        else:
            # Hard: use minimax
            choice = self._best_move_minimax()

        # Ensure current is AI symbol and perform the move
        self.current = self.ai_symbol
        self.on_click(choice)

    def _best_move_minimax(self):
        # returns index of best move for AI using depth-aware minimax
        def minimax(board, player, depth):
            winner, _ = self._check_winner_for_minimax(board)
            if winner == self.ai_symbol:
                return 10 - depth, None
            elif winner == self.human_symbol:
                return depth - 10, None
            elif all(v is not None for v in board):
                return 0, None

            if player == self.ai_symbol:
                best_score = -999
                best_move = None
                for i in range(9):
                    if board[i] is None:
                        board[i] = player
                        score, _ = minimax(board, self.human_symbol, depth + 1)
                        board[i] = None
                        if score > best_score:
                            best_score = score
                            best_move = i
                return best_score, best_move
            else:
                best_score = 999
                best_move = None
                for i in range(9):
                    if board[i] is None:
                        board[i] = player
                        score, _ = minimax(board, self.ai_symbol, depth + 1)
                        board[i] = None
                        if score < best_score:
                            best_score = score
                            best_move = i
                return best_score, best_move

        _, move = minimax(self.board[:], self.ai_symbol, 0)
        # fallback
        if move is None:
            moves = [i for i, v in enumerate(self.board) if v is None]
            return random.choice(moves)
        return move

    def _check_winner_for_minimax(self, board):
        wins = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)
        ]
        for a, b, c in wins:
            if board[a] and board[a] == board[b] == board[c]:
                return board[a], (a, b, c)
        return None, None

    def update_scores(self):
        self.score_x.config(text=f"X: {self.scores['X']}")
        self.score_o.config(text=f"O: {self.scores['O']}")

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    app = TicTacToeApp()
    app.run()