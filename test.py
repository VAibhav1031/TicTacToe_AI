
import random

class TicTacToe:
    def __init__(self, size, computer_player=False):
        """
        Constructor for initiating the size, Board, and players instance.
        """
        self.size = size
        self.board = [[" "] * self.size for _ in range(self.size)]
        self.Players = {1: None, 2: None}
        self.PlayersName = {1: None, 2: None}
        self.computer_player = computer_player  # True if playing against the computer
        self.last_move = None  # Track the last move

    def printBoardStatus(self):
        """
        Print the current state of the board.
        """
        sep = "\n" + "-" * (self.size * 4 - 3) + "\n"
        print("\n" + sep.join(" | ".join(col) for col in self.board) + "\n")

    def makeMove(self, player: int):
        """
        Handle the move for a player (human or computer).
        """
        if self.computer_player and player == 2:  # Computer's turn
            print("Computer's turn...")
            row, col = self.find_best_move()
            print(f"Computer chooses: ({row + 1}, {col + 1})")
            return row, col
        else:  # Human's turn
            while True:
                try:
                    row = int(input(f"Enter the ROW Player {player} ({self.Players[player]}): "))
                    col = int(input(f"Enter the COLUMN Player {player} ({self.Players[player]}): "))
                except ValueError as e:
                    print(f"Error: {e}")
                    continue
                if 1 <= row <= len(self.board) and 1 <= col <= len(self.board):
                    return row - 1, col - 1
                print(f"Enter a valid range between 1 and {len(self.board)}")

    def ChooseSymbol(self):
        """
        Randomly choose which player gets which symbol.
        """
        symbol = ["X", "O"]
        random.shuffle(symbol)
        return symbol[0], symbol[1]

    def playOneRound(self, player: int) -> None:
        """
        Handle a single round of the game.
        """
        while True:
            row, col = self.makeMove(player)
            if self.board[row][col] == " ":
                self.board[row][col] = self.Players[player]
                self.last_move = (row, col)  # Track the last move
                break
            print("Space is occupied.")

    def check_winner(self, board, last_move):
        """
        Check for a winner based on the last move.
        """
        row, col = last_move
        player = board[row][col]
        n = len(board)
        win_length = 3  # Number of consecutive symbols required to win

        # Check row
        count = 1
        for i in range(1, win_length):
            if col - i >= 0 and board[row][col - i] == player:
                count += 1
            else:
                break
        for i in range(1, win_length):
            if col + i < n and board[row][col + i] == player:
                count += 1
            else:
                break
        if count >= win_length:
            return player

        # Check column
        count = 1
        for i in range(1, win_length):
            if row - i >= 0 and board[row - i][col] == player:
                count += 1
            else:
                break
        for i in range(1, win_length):
            if row + i < n and board[row + i][col] == player:
                count += 1
            else:
                break
        if count >= win_length:
            return player

        # Check diagonal (top-left to bottom-right)
        count = 1
        for i in range(1, win_length):
            if row - i >= 0 and col - i >= 0 and board[row - i][col - i] == player:
                count += 1
            else:
                break
        for i in range(1, win_length):
            if row + i < n and col + i < n and board[row + i][col + i] == player:
                count += 1
            else:
                break
        if count >= win_length:
            return player

        # Check diagonal (bottom-left to top-right)
        count = 1
        for i in range(1, win_length):
            if row + i < n and col - i >= 0 and board[row + i][col - i] == player:
                count += 1
            else:
                break
        for i in range(1, win_length):
            if row - i >= 0 and col + i < n and board[row - i][col + i] == player:
                count += 1
            else:
                break
        if count >= win_length:
            return player

        return None

    def is_board_full(self, board):
        """
        Check if the board is full.
        """
        return all(cell != " " for row in board for cell in row)

    def minimax(self, board, is_maximizing, last_move):
        """
        Minimax algorithm to determine the best move for the computer.
        """
        winner = self.check_winner(board, last_move)
        if winner == self.Players[1]:  # Human wins
            return -1
        elif winner == self.Players[2]:  # Computer wins
            return 1
        elif self.is_board_full(board):  # Draw
            return 0

        if is_maximizing:
            best_score = -float("inf")
            for row in range(self.size):
                for col in range(self.size):
                    if board[row][col] == " ":
                        board[row][col] = self.Players[2]  # Computer's move
                        score = self.minimax(board, False, (row, col))
                        board[row][col] = " "  # Undo move
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float("inf")
            for row in range(self.size):
                for col in range(self.size):
                    if board[row][col] == " ":
                        board[row][col] = self.Players[1]  # Human's move
                        score = self.minimax(board, True, (row, col))
                        board[row][col] = " "  # Undo move
                        best_score = min(score, best_score)
            return best_score

    def find_best_move(self):
        """
        Find the best move for the computer using Minimax.
        """
        # First, check if the computer can win in the next move
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == " ":
                    self.board[row][col] = self.Players[2]  # Computer's move
                    if self.check_winner(self.board, (row, col)) == self.Players[2]:
                        self.board[row][col] = " "  # Undo move
                        return (row, col)
                    self.board[row][col] = " "  # Undo move

        # If no immediate win, use Minimax to find the best move
        best_score = -float("inf")
        best_move = (-1, -1)
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == " ":
                    self.board[row][col] = self.Players[2]  # Computer's move
                    score = self.minimax(self.board, False, (row, col))
                    self.board[row][col] = " "  # Undo move
                    if score > best_score:
                        best_score = score
                        best_move = (row, col)
        return best_move

    def main(self):
        """
        Main function to run the game.
        """
        self.Players[1], self.Players[2] = self.ChooseSymbol()
        self.PlayersName[1] = input("Player 1, enter your name: ")
        if not self.computer_player:
            self.PlayersName[2] = input("Player 2, enter your name: ")
        else:
            self.PlayersName[2] = "Computer"

        player = 1
        self.printBoardStatus()
        while True:
            print(f"{self.PlayersName[player].upper()}'s turn (Symbol: {self.Players[player]})\n")
            self.playOneRound(player)
            self.printBoardStatus()
            if self.check_winner(self.board, self.last_move) == self.Players[player]:
                print(f"Player {player} ({self.PlayersName[player]}) won!!!")
                break
            if self.is_board_full(self.board):
                print("Draw!!!")
                break
            player = player % len(self.Players) + 1


if __name__ == "__main__":
    def play():
        print("Welcome to Tic Tac Toe!")
        while True:
            try:
                size = int(input("\nEnter the size of the board (N x N): "))
                if size < 3:
                    print("Size must be at least 3.")
                    continue
                break
            except ValueError as e:
                print(f"Error: {e}")

        computer_player = input("Play against the computer? (Y/N): ").strip().upper() == "Y"

        while True:
            ttt = TicTacToe(size, computer_player)
            ttt.main()
            n = input("\nWant to play again? (Y/N): ").strip().upper()
            if n != "Y":
                break

    play()
