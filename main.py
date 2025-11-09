import tkinter as tk
from tkinter import ttk, messagebox
import random

class TicTacToeAI:
    def __init__(self, ai_player='O', human_player='X', difficulty='Hard'):
        self.ai = ai_player
        self.human = human_player
        self.difficulty = difficulty

    def choose_move(self, board):
        available = [i for i, v in enumerate(board) if v == ' ']
        if not available:
            return None

        if self.difficulty == 'Easy':
            return random.choice(available)

        elif self.difficulty == 'Medium':
            best_score = -float('inf')
            best_move = None
            for move in available:
                board[move] = self.ai
                score = self.minimax(board, 0, False, -float('inf'), float('inf'), limit=3)
                board[move] = ' '
                if score > best_score:
                    best_score, best_move = score, move
            return best_move

        else:  # Hard
            best_score = -float('inf')
            best_move = None
            for move in available:
                board[move] = self.ai
                score = self.minimax(board, 0, False, -float('inf'), float('inf'))
                board[move] = ' '
                if score > best_score:
                    best_score, best_move = score, move
            return best_move

    def evaluate(self, board):
        winner = TicTacToeGame.check_winner_static(board)
        if winner == self.ai:
            return 10
        elif winner == self.human:
            return -10
        else:
            return 0

    def heuristic(self, board):
        score = 0
        lines = [(0,1,2),(3,4,5),(6,7,8),
                 (0,3,6),(1,4,7),(2,5,8),
                 (0,4,8),(2,4,6)]
        for a,b,c in lines:
            line = [board[a], board[b], board[c]]
            if line.count(self.ai) == 2 and line.count(' ') == 1:
                score += 5
            if line.count(self.human) == 2 and line.count(' ') == 1:
                score -= 4
        return score

    def minimax(self, board, depth, is_max, alpha, beta, limit=None):
        score = self.evaluate(board)
        if abs(score) == 10 or ' ' not in board:
            return score
        if limit is not None and depth >= limit:
            return self.heuristic(board)

        if is_max:
            best = -float('inf')
            for i in range(9):
                if board[i] == ' ':
                    board[i] = self.ai
                    best = max(best, self.minimax(board, depth+1, False, alpha, beta, limit))
                    board[i] = ' '
                    alpha = max(alpha, best)
                    if beta <= alpha:
                        break
            return best
        else:
            best = float('inf')
            for i in range(9):
                if board[i] == ' ':
                    board[i] = self.human
                    best = min(best, self.minimax(board, depth+1, True, alpha, beta, limit))
                    board[i] = ' '
                    beta = min(beta, best)
                    if beta <= alpha:
                        break
            return best

class TicTacToeGame:
    def __init__(self, root):
        self.root = root
        self.root.title('Tic Tac Toe - AI Mini Project')
        self.root.attributes('-fullscreen', True)

        self.board = [' '] * 9
        self.buttons = [None] * 9
        self.current_player = 'X'
        self.game_over = False

        self.mode_var = tk.StringVar(value='Human vs AI')
        self.difficulty_var = tk.StringVar(value='Hard')
        self.symbol_var = tk.StringVar(value='X')

        ai_player = 'O' if self.symbol_var.get() == 'X' else 'X'
        self.ai = TicTacToeAI(
            ai_player=ai_player,
            human_player=self.symbol_var.get(),
            difficulty=self.difficulty_var.get()
        )

        self.create_background()
        self.create_widgets()
        self.update_status("Player X's turn")

        if self.mode_var.get() == 'Human vs AI' and self.ai.ai == 'X':
            self.root.after(500, self.maybe_ai_move)

    def create_background(self):
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.canvas = tk.Canvas(self.root, width=sw, height=sh, highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
        for i in range(0, 100):
            r = min(40 + i*2, 255)
            g = min(50 + i*2, 255)
            b = min(70 + int(i*1.5), 255)
            color = f'#{r:02x}{g:02x}{b:02x}'
            self.canvas.create_rectangle(0, i*(sh//100), sw, (i+1)*(sh//100), outline='', fill=color)

    def create_widgets(self):
        style = ttk.Style()
        style.configure('TButton', font=('Poppins', 12, 'bold'), padding=6)

        container = tk.Frame(self.canvas, bg='#121212')
        container.place(relx=0.5, rely=0.5, anchor='center')

        tk.Label(container, text='Tic Tac Toe — AI Mini Project',
                 font=('Poppins', 28, 'bold'), fg='white', bg='#121212').pack(pady=(10, 18))

        top_frame = tk.Frame(container, bg='#1e1e1e', pady=10)
        top_frame.pack(fill='x', padx=10, pady=(0, 12))

        tk.Label(top_frame, text='Mode:', font=('Poppins', 12), fg='white', bg='#1e1e1e').grid(row=0, column=0, sticky='w', padx=6)
        mode_menu = ttk.OptionMenu(top_frame, self.mode_var, self.mode_var.get(),
                                   'Human vs Human', 'Human vs AI', command=self.on_mode_change)
        mode_menu.grid(row=0, column=1, padx=6)

        tk.Label(top_frame, text='Difficulty:', font=('Poppins', 12), fg='white', bg='#1e1e1e').grid(row=0, column=2, sticky='w', padx=6)
        diff_menu = ttk.OptionMenu(top_frame, self.difficulty_var, self.difficulty_var.get(),
                                   'Easy', 'Medium', 'Hard', 'N/A', command=self.on_difficulty_change)
        diff_menu.grid(row=0, column=3, padx=6)

        tk.Label(top_frame, text='Your Symbol:', font=('Poppins', 12), fg='white', bg='#1e1e1e').grid(row=0, column=4, sticky='w', padx=6)
        sym_menu = ttk.OptionMenu(top_frame, self.symbol_var, self.symbol_var.get(),
                                  'X', 'O', command=self.on_symbol_change)
        sym_menu.grid(row=0, column=5, padx=6)

        ttk.Button(top_frame, text='Restart', command=self.restart_game).grid(row=0, column=6, padx=10)
        ttk.Button(top_frame, text='Exit', command=self.root.destroy).grid(row=0, column=7, padx=6)

        board_frame = tk.Frame(container, bg='#121212')
        board_frame.pack(pady=10)

        for i in range(9):
            btn = tk.Button(
                board_frame, text=' ', font=('Poppins', 36, 'bold'), width=4, height=2,
                bg='#1c1c3c', fg='white', activebackground='#2c2c5c', relief='flat',
                command=lambda i=i: self.on_cell_clicked(i)
            )
            btn.grid(row=i//3, column=i%3, padx=12, pady=12)
            btn.bind('<Enter>', lambda e, b=btn: b.config(bg='#3a3a7a') if b['state'] == 'normal' else None)
            btn.bind('<Leave>', lambda e, b=btn: b.config(bg='#1c1c3c') if b['state'] == 'normal' else None)
            self.buttons[i] = btn

        self.status_var = tk.StringVar()
        tk.Label(container, textvariable=self.status_var, font=('Poppins', 14, 'bold'),
                 fg='white', bg='#121212').pack(pady=(8, 6))

        tk.Label(container, text="Press ESC to exit fullscreen", font=('Poppins', 10),
                 fg='lightgray', bg='#121212').pack(pady=(2, 8))

        self.root.bind('<Escape>', lambda e: self.root.attributes('-fullscreen', False))

    def on_mode_change(self, *_):
        if self.mode_var.get() == 'Human vs Human':
            self.difficulty_var.set('N/A')
        else:
            if self.difficulty_var.get() == 'N/A':
                self.difficulty_var.set('Hard')
        self._update_ai_settings()

    def on_difficulty_change(self, *_):
        diff = self.difficulty_var.get()
        if diff != 'N/A':
            self.ai.difficulty = diff
        self._update_ai_settings()

    def on_symbol_change(self, *_):
        human = self.symbol_var.get()
        ai = 'O' if human == 'X' else 'X'
        self.ai.human, self.ai.ai = human, ai
        if self.difficulty_var.get() != 'N/A':
            self.ai.difficulty = self.difficulty_var.get()
        # fresh turn logic
        if not self.game_over:
            self.current_player = 'X'
            self.update_status(f"Player {self.current_player}'s turn")
            if self.mode_var.get() == 'Human vs AI' and ai == 'X':
                self.root.after(300, self.maybe_ai_move)

    def _update_ai_settings(self):
        human = self.symbol_var.get()
        ai = 'O' if human == 'X' else 'X'
        self.ai.human = human
        self.ai.ai = ai
        if self.difficulty_var.get() != 'N/A':
            self.ai.difficulty = self.difficulty_var.get()

    def on_cell_clicked(self, idx):
        if self.game_over or self.board[idx] != ' ':
            return

        mode = self.mode_var.get()
        if mode == 'Human vs Human':
            self.make_move(idx, self.current_player)
            if not self.game_over and ' ' in self.board:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                self.update_status(f"Player {self.current_player}'s turn")
        else:
            # human move only when it's human's turn
            if self.current_player != self.ai.human:
                return
            self.make_move(idx, self.ai.human)
            if not self.game_over:
                self.current_player = self.ai.ai
                self.update_status("AI's turn...")
                self.root.after(300, self.maybe_ai_move)

    def maybe_ai_move(self):
        if self.game_over or self.current_player != self.ai.ai:
            return
        move = self.ai.choose_move(self.board[:])
        if move is not None and self.board[move] == ' ':
            self.make_move(move, self.ai.ai)
        if not self.game_over:
            self.current_player = self.ai.human
            self.update_status(f"Player {self.current_player}'s turn")

    def make_move(self, idx, symbol):
        if self.game_over or self.board[idx] != ' ':
            return
        self.board[idx] = symbol
        self.buttons[idx].config(text=symbol, state='disabled', disabledforeground='white', bg='#2a2a6a')
        winner = self.check_winner()
        if winner:
            self.game_over = True
            if winner != 'Draw':
                self.highlight_winner()
            msg = 'Game Draw!' if winner == 'Draw' else f'Player {winner} Wins!'
            self.update_status(msg)
            messagebox.showinfo('Result', msg)
            for b in self.buttons:
                b.config(state='disabled')

    def restart_game(self):
        self.board = [' '] * 9
        for b in self.buttons:
            b.config(text=' ', state='normal', bg='#1c1c3c')
        self.current_player = 'X'
        self.game_over = False
        self.update_status("Player X's turn")
        self._update_ai_settings()
        if self.mode_var.get() == 'Human vs AI' and self.ai.ai == 'X':
            self.root.after(400, self.maybe_ai_move)

    def update_status(self, text):
        self.status_var.set(text)

    def check_winner(self):
        return self.check_winner_static(self.board)

    @staticmethod
    def check_winner_static(board):
        lines = [(0,1,2),(3,4,5),(6,7,8),
                 (0,3,6),(1,4,7),(2,5,8),
                 (0,4,8),(2,4,6)]
        for a,b,c in lines:
            if board[a] == board[b] == board[c] and board[a] != ' ':
                return board[a]
        if ' ' not in board:
            return 'Draw'
        return None

    def highlight_winner(self):
        lines = [(0,1,2),(3,4,5),(6,7,8),
                 (0,3,6),(1,4,7),(2,5,8),
                 (0,4,8),(2,4,6)]
        for a,b,c in lines:
            if self.board[a] == self.board[b] == self.board[c] and self.board[a] != ' ':
                for i in (a,b,c):
                    self.buttons[i].config(bg='#3c9141')  # subtle highlight
                break

if __name__ == '__main__':
    root = tk.Tk()
    app = TicTacToeGame(root)
    root.mainloop()
