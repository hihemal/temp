import tkinter as tk
from tkinter import messagebox
import random

# The main class for our Tic Tac Toe game
class TicTacToeApp:
    def __init__(self, root):
        """
        Initialize the game application.
        
        Args:
            root: The main window object from tkinter.
        """
        self.root = root
        self.root.title("Tic Tac Toe") # Set the title of the window
        
        # Variable to keep track of whose turn it is
        # We start with 'X' (Human)
        self.current_player = "X" 
        
        # We will represent the board as a list of 9 items
        # Initially, all spots are empty strings ""
        # The board indices look like this:
        # 0 | 1 | 2
        # ---------
        # 3 | 4 | 5
        # ---------
        # 6 | 7 | 8
        self.board = [""] * 9
        
        # We also need a way to store the Button widgets so we can change their text later
        self.buttons = []
        
        # Game mode: "PvP" (Player vs Player) or "PvE" (Player vs Computer)
        # Defaulting to Player vs Computer for now
        self.game_mode = "PvE" 
        
        # Setup the Graphical User Interface (GUI)
        self.setup_ui()
        
    def setup_ui(self):
        """
        Create and arrange all the buttons and labels on the screen.
        """
        # 1. Create a label at the top to show status (e.g., "X's Turn")
        self.status_label = tk.Label(self.root, text="X's Turn", font=("Helvetica", 16))
        self.status_label.pack(pady=10) # Add some vertical padding nicely
        
        # 2. Create a frame to hold the grid of buttons
        # A frame is like a container for other widgets
        grid_frame = tk.Frame(self.root)
        grid_frame.pack()
        
        # 3. Create the 9 buttons for the grid
        for i in range(9):
            # Create a button.
            # text="": Initially empty
            # font: Make the text big
            # width, height: Set the size of the button
            # command: The function to call when clicked. 
            # We use a 'lambda' (anonymous function) to pass the specific index 'i' to the function.
            btn = tk.Button(grid_frame, text="", font=("Helvetica", 20), width=5, height=2,
                            command=lambda index=i: self.on_button_click(index))
            
            # Add the button to the grid layout.
            # row is i // 3 (integer division): 0, 0, 0, 1, 1, 1, 2, 2, 2
            # col is i % 3 (modulo/remainder): 0, 1, 2, 0, 1, 2, ...
            btn.grid(row=i//3, column=i%3, padx=5, pady=5)
            
            # Store the button in our list so we can access it later
            self.buttons.append(btn)
            
        # 4. Create a Reset Button at the bottom
        reset_btn = tk.Button(self.root, text="Reset Game", font=("Helvetica", 12), command=self.reset_game)
        reset_btn.pack(pady=10)

        # 5. Create a Menu to change Game Mode
        # We create a top-level menu bar
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)
        
        # Create a "Settings" menu inside the menu bar
        settings_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Settings", menu=settings_menu)
        
        # Add options to the Settings menu
        # When clicked, they call self.set_mode with specific values
        settings_menu.add_command(label="Play vs Computer", command=lambda: self.set_mode("PvE"))
        settings_menu.add_command(label="Play vs Human", command=lambda: self.set_mode("PvP"))
    
    def set_mode(self, mode):
        """
        Change the game mode and reset automatically.
        """
        self.game_mode = mode
        messagebox.showinfo("Mode Changed", f"Game Mode set to: {mode}")
        self.reset_game()

    def on_button_click(self, index):
        """
        This function is called when a player clicks a button on the grid.
        
        Args:
            index: The position (0-8) of the button that was clicked.
        """
        # If the clicked spot is already taken, do nothing
        if self.board[index] != "":
            return
        
        # update the board data and the visual button text
        self.board[index] = self.current_player
        self.buttons[index].config(text=self.current_player)
        
        # Check if this move won the game
        if self.check_winner(self.current_player):
            messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
            self.reset_game()
            return
        
        # Check if the game is a draw (board is full)
        if "" not in self.board:
            messagebox.showinfo("Game Over", "It's a Draw!")
            self.reset_game()
            return
        
        # Switch turns
        self.switch_player()
        
        # If it's now the Computer's turn and we are in PvE mode, let the computer move
        if self.game_mode == "PvE" and self.current_player == "O":
            # We use root.after to add a small delay so it doesn't feel instant/robotic
            self.root.after(500, self.computer_move)

    def switch_player(self):
        """Switch the current player from X to O or O to X."""
        if self.current_player == "X":
            self.current_player = "O"
        else:
            self.current_player = "X"
        
        # Update the status label text
        self.status_label.config(text=f"{self.current_player}'s Turn")

    def check_winner(self, player):
        """
        Check if the given player has won.
        
        Args:
            player: 'X' or 'O'
        Returns:
            True if the player has a winning line, False otherwise.
        """
        # All possible winning combinations (indices)
        winning_combos = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8), # Rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8), # Columns
            (0, 4, 8), (2, 4, 6)             # Diagonals
        ]
        
        for a, b, c in winning_combos:
            # Check if all three spots in a combination belong to the player
            if self.board[a] == player and self.board[b] == player and self.board[c] == player:
                return True
        return False

    def computer_move(self):
        """The computer (Player O) makes a move."""
        # Simple Logic: Pick a random empty spot
        # 1. Find all indices where the board is empty
        available_moves = [i for i, x in enumerate(self.board) if x == ""]
        
        if available_moves:
            # 2. Randomly choose one
            move = random.choice(available_moves)
            # 3. 'Click' that button programmatically
            self.on_button_click(move)

    def reset_game(self):
        """Reset the game state to the beginning."""
        self.current_player = "X"
        self.board = [""] * 9
        self.status_label.config(text="X's Turn")
        
        # Clear the text on all buttons
        for btn in self.buttons:
            btn.config(text="")

# Execution starts here
if __name__ == "__main__":
    # Create the main window setup
    root = tk.Tk()
    
    # Initialize our game application
    app = TicTacToeApp(root)
    
    # Start the main event loop
    # This keeps the window open and listening for clicks
    root.mainloop()
