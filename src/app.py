"""GAMEX interactive Tkinter demonstration."""
import tkinter as tk
from tkinter import ttk, messagebox
from .engine import minimax
from .ttt import TicTacToe


class GameApp:
    def __init__(self, root):
        self.root = root
        root.title("GAMEX | Minimax Game Engine")
        root.geometry("980x760")
        root.minsize(860, 680)
        root.configure(bg="#e9e9e9")
        self.state = TicTacToe()
        self.depth = tk.IntVar(value=9)
        self.ai = "O"
        self.human = "X"
        self._thinking = False
        self.human_score = 0
        self.ai_score = 0
        self.draw_score = 0
        self._build()
        self.refresh()

    def _build(self):
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("TScale", troughcolor="#d8d8d8", background="#111111",
                        bordercolor="#d8d8d8", lightcolor="#111111",
                        darkcolor="#111111")

        header = tk.Frame(self.root, bg="#e9e9e9")
        header.pack(fill="x", padx=38, pady=(24, 16))

        brand = tk.Frame(header, bg="#e9e9e9")
        brand.pack(side="left")
        tk.Label(brand, text="GAMEX", font=("Segoe UI", 32, "bold"),
                 fg="#111111", bg="#e9e9e9").pack(anchor="w")
        tk.Label(brand, text="MINIMAX GAME ENGINE", font=("Segoe UI", 10, "bold"),
                 fg="#555555", bg="#e9e9e9").pack(anchor="w", pady=(2, 0))

        scores = tk.Frame(header, bg="#e9e9e9")
        scores.pack(side="right")
        self.score_labels = {}
        for key, label in (("human", "YOU"),
                           ("draw", "DRAWS"),
                           ("ai", "AI")):
            card = tk.Frame(scores, bg="#ffffff", width=92, height=58,
                            highlightthickness=1, highlightbackground="#d0d0d0")
            card.pack(side="left", padx=6)
            card.pack_propagate(False)
            tk.Label(card, text=label, font=("Segoe UI", 9, "bold"),
                     fg="#666666", bg="#ffffff").pack(pady=(8, 0))
            value = tk.Label(card, text="0", font=("Segoe UI", 16, "bold"),
                             fg="#111111", bg="#ffffff")
            value.pack()
            self.score_labels[key] = value

        self.status_card = tk.Frame(self.root, bg="#ffffff", height=58,
                                    highlightthickness=1, highlightbackground="#d0d0d0")
        self.status_card.pack(fill="x", padx=38, pady=(0, 18))
        self.status_card.pack_propagate(False)

        self.status_dot = tk.Canvas(self.status_card, width=12, height=12,
                                    highlightthickness=0, bg="#ffffff")
        self.status_dot.place(relx=.018, rely=.5, anchor="w")
        self.status = tk.Label(self.status_card, text="",
                               font=("Segoe UI", 13, "bold"), fg="#111111",
                               bg="#ffffff")
        self.status.place(relx=.052, rely=.5, anchor="w")

        body = tk.Frame(self.root, bg="#e9e9e9")
        body.pack(fill="both", expand=True, padx=38, pady=(0, 24))

        left = tk.Frame(body, bg="#e9e9e9")
        left.pack(side="left", fill="both", expand=True)

        self.board_frame = tk.Frame(left, bg="#c7c7c7", padx=12, pady=12,
                                    highlightthickness=1, highlightbackground="#b8b8b8")
        self.board_frame.pack(anchor="center")
        self.buttons = []
        for i in range(9):
            btn = tk.Button(self.board_frame, text="", font=("Segoe UI", 42, "bold"),
                            width=3, height=1, bg="#ffffff", fg="#111111",
                            activebackground="#d9d9d9", activeforeground="#111111",
                            relief="flat", bd=0, cursor="hand2",
                            command=lambda idx=i: self.human_move(idx))
            btn.grid(row=i//3, column=i%3, padx=6, pady=6)
            btn.bind("<Enter>", lambda e, b=btn: self._hover(b, True))
            btn.bind("<Leave>", lambda e, b=btn: self._hover(b, False))
            self.buttons.append(btn)

        right = tk.Frame(body, bg="#ffffff", width=270,
                         highlightthickness=1, highlightbackground="#d0d0d0")
        right.pack(side="right", fill="y", padx=(22, 0))
        right.pack_propagate(False)

        tk.Label(right, text="GAME ANALYSIS", font=("Segoe UI", 12, "bold"),
                 fg="#111111", bg="#ffffff").pack(anchor="w", padx=20, pady=(22, 14))

        self.stats = tk.Label(right, text="", font=("Consolas", 11),
                              fg="#333333", bg="#ffffff", justify="left",
                              anchor="nw")
        self.stats.pack(fill="x", padx=20)

        tk.Label(right, text="SEARCH DEPTH", font=("Segoe UI", 11, "bold"),
                 fg="#111111", bg="#ffffff").pack(anchor="w", padx=20, pady=(22, 10))

        control = tk.Frame(right, bg="#ffffff")
        control.pack(fill="x", padx=20)
        self.depth_label = tk.Label(control, text="9", font=("Segoe UI", 13, "bold"),
                                    fg="#111111", bg="#ffffff", width=3)
        self.depth_label.pack(side="right")
        depth_box = ttk.Scale(control, from_=1, to=9, variable=self.depth,
                              command=self._depth_changed)
        depth_box.pack(side="left", fill="x", expand=True)

        tk.Frame(right, bg="#d0d0d0", height=1).pack(fill="x", padx=20, pady=20)

        tk.Button(right, text="Analyze position", command=self.analyze,
                  font=("Segoe UI", 11, "bold"), bg="#ededed", fg="#111111",
                  activebackground="#dddddd", activeforeground="#111111",
                  relief="flat", cursor="hand2", pady=11).pack(fill="x", padx=20)
        tk.Button(right, text="New game", command=self.reset,
                  font=("Segoe UI", 11, "bold"), bg="#111111", fg="#ffffff",
                  activebackground="#333333", activeforeground="#ffffff",
                  relief="flat", cursor="hand2", pady=11).pack(fill="x", padx=20, pady=10)

        legend = tk.Frame(right, bg="#ffffff")
        legend.pack(side="bottom", fill="x", padx=20, pady=18)
        tk.Label(legend, text="YOU", font=("Segoe UI", 9, "bold"),
                 fg="#111111", bg="#ffffff").pack(side="left")
        tk.Label(legend, text="  X  |  O  ", font=("Segoe UI", 9),
                 fg="#777777", bg="#ffffff").pack(side="left")
        tk.Label(legend, text="AI", font=("Segoe UI", 9, "bold"),
                 fg="#111111", bg="#ffffff").pack(side="left")

    def _depth_changed(self, _value):
        self.depth_label.config(text=str(int(float(self.depth.get()))))
        self.refresh()

    def _hover(self, button, entering):
        if str(button["state"]) == "normal":
            button.config(bg="#e2e2e2" if entering else "#ffffff")

    def _set_status(self, text, dot_color):
        self.status.config(text=text)
        self.status_dot.delete("all")
        self.status_dot.create_oval(2, 2, 10, 10, fill=dot_color,
                                    outline=dot_color)

    def _winning_line(self):
        from .ttt import WIN_LINES
        for a, b, c in WIN_LINES:
            vals = [self.state.board[a], self.state.board[b], self.state.board[c]]
            if vals[0] != " " and vals[0] == vals[1] == vals[2]:
                return (a, b, c)
        return None

    def refresh(self):
        win_line = self._winning_line()
        for i, btn in enumerate(self.buttons):
            val = self.state.board[i]
            is_win = win_line is not None and i in win_line
            btn.config(text="" if val == " " else val,
                       fg="#111111",
                       bg="#bdbdbd" if is_win else "#ffffff",
                       state="normal" if val == " " and not self.state.is_terminal() and self.state.player == self.human else "disabled")
        win = self.state.winner()
        if win:
            if win == self.human:
                self._set_status("You win! Well played.", "#111111")
            else:
                self._set_status("AI wins this round.", "#111111")
        elif self.state.is_terminal():
            self._set_status("Round drawn.", "#777777")
        elif self._thinking:
            self._set_status("AI is calculating...", "#555555")
        else:
            self._set_status("Your turn — place X", "#111111")
        if self.state.is_terminal():
            move_count = sum(cell != " " for cell in self.state.board)
            self.stats.config(text=f"STATUS\nRound complete\n\n"
                                   f"MOVES\n{move_count} / 9\n\n"
                                   f"SEARCH DEPTH\n{int(self.depth.get())}")
        else:
            move_count = sum(cell != " " for cell in self.state.board)
            self.stats.config(text=f"STATUS\nIn progress\n\n"
                                   f"MOVES\n{move_count} / 9\n\n"
                                   f"SEARCH DEPTH\n{int(self.depth.get())}")

    def human_move(self, move):
        if move not in self.state.legal_moves() or self.state.player != self.human: return
        self.state = self.state.apply_move(move)
        self.refresh()
        if not self.state.is_terminal():
            self._thinking = True
            self._set_status("AI is calculating...", "#555555")
            for btn in self.buttons:
                btn.config(state="disabled")
            self.root.after(250, self.ai_move)
        else:
            self._update_score()

    def ai_move(self):
        if self.state.is_terminal(): return
        move, value, stats = minimax(self.state, int(self.depth.get()), self.ai)
        if move is not None: self.state = self.state.apply_move(move)
        self._thinking = False
        self.refresh()
        if self.state.is_terminal():
            self._update_score()
            best_move_text = "None"
        else:
            best_move_text = f"R{move//3+1} C{move%3+1}" if move is not None else "None"
        self.stats.config(text=f"NODES\n{stats.nodes:,}\n\n"
                               f"MAX DEPTH\n{stats.max_depth}\n\n"
                               f"UTILITY\n{value:+.2f}\n\n"
                               f"AI MOVE\n{best_move_text}")

    def analyze(self):
        if self.state.is_terminal():
            messagebox.showinfo("Analysis", "The current board is terminal.")
            return
        move, value, stats = minimax(self.state, int(self.depth.get()), self.ai)
        best_move_text = f"R{move//3+1} C{move%3+1}" if move is not None else "None"
        self.stats.config(text=f"NODES\n{stats.nodes:,}\n\n"
                               f"MAX DEPTH\n{stats.max_depth}\n\n"
                               f"UTILITY\n{value:+.2f}\n\n"
                               f"BEST MOVE\n{best_move_text}")

    def _update_score(self):
        win = self.state.winner()
        if win == self.human:
            self.human_score += 1
            self.score_labels["human"].config(text=str(self.human_score))
        elif win == self.ai:
            self.ai_score += 1
            self.score_labels["ai"].config(text=str(self.ai_score))
        else:
            self.draw_score += 1
            self.score_labels["draw"].config(text=str(self.draw_score))

    def reset(self):
        self.state = TicTacToe()
        self._thinking = False
        self.refresh()

def main():
    root = tk.Tk()
    GameApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
