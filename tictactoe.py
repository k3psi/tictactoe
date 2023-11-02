import tkinter as tk
import random
import time

def choose_player(player1, player2):
    global p1, p2
    p1, p2 = "", ""
    a = random.randint(0, 1)
    if a == 0:
        p1 = "X"
        p2 = "O"
    else:
        p1 = "O"
        p2 = "X"

def display_board(board):
    for i in range(3):
        for j in range(3):
            cell = board[i][j]
            buttons[i][j] = tk.Button(root, text=cell, width=10, height=3,
                               command=lambda row=i, col=j: on_click(row, col))
            buttons[i][j].grid(row=i, column=j)

def check_winner(board, player):
    for i in range(3):
        if all(board[i][j] == player for j in range(3)) or \
                all(board[j][i] == player for j in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or \
            all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def on_click(row, col):
    if board[row][col] == " " and not winner and current_player == p1:
        board[row][col] = current_player
        buttons[row][col].config(text=current_player)
        buttons[row][col].config(state=tk.DISABLED)  # Disable the clicked button
        if check_winner(board, current_player):
            winner_label.config(text=f"Player {current_player} wins!")
            root.after(3000, restart_game)  # Restart the game after 3 seconds
        elif all(cell != " " for row in board for cell in row):
            winner_label.config(text="It's a draw!")
            root.after(3000, restart_game)  # Restart the game after 3 seconds
        else:
            toggle_player()
            root.after(random.randint(1500, 3000), ai_play)  # Delay for CPU's move

def toggle_player():
    global current_player
    current_player = p1 if current_player == p2 else p2
    player_label.config(text=f"Current player: {current_player}")

def ai_play():
    # Basic AI: Randomly choose an empty cell
    empty_cells = [(i, j) for i in range(3) for j in range(3) if board[i][j] == " "]
    if empty_cells:
        row, col = random.choice(empty_cells)
        board[row][col] = current_player
        buttons[row][col].config(text=current_player)
        buttons[row][col].config(state=tk.DISABLED)  # Disable the CPU's move
        if check_winner(board, current_player):
            winner_label.config(text=f"Player {current_player} wins!")
            root.after(3000, restart_game)  # Restart the game after 3 seconds
        elif all(cell != " " for row in board for cell in row):
            winner_label.config(text="It's a draw!")
            root.after(3000, restart_game)  # Restart the game after 3 seconds
        else:
            toggle_player()
            for i in range(3):
                for j in range(3):
                    if board[i][j] == " ":
                        buttons[i][j].config(state=tk.NORMAL)  # Re-enable user input

def restart_game():
    global board, current_player, winner
    board = [[" " for _ in range(3)] for _ in range(3)]
    display_board(board)
    winner_label.config(text="")
    winner = False
    choose_player(player1, player2)
    current_player = p1
    player_label.config(text=f"Current player: {current_player}")
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(state=tk.NORMAL)  # Re-enable user input

root = tk.Tk()
root.title("Tic-Tac-Toe")

player1 = "Player 1"
player2 = "CPU"
choose_player(player1, player2)
current_player = p1

board = [[" " for _ in range(3)] for _ in range(3)]
buttons = [[None] * 3 for _ in range(3)]

player_label = tk.Label(root, text=f"Current player: {current_player}")
player_label.grid(row=3, columnspan=3)
winner_label = tk.Label(root, text="")
winner_label.grid(row=4, columnspan=3)

display_board(board)
winner = False

root.mainloop()
