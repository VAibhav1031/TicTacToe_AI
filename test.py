##################
# Bit improvement
#################


# you know  we have already the imrovement measures,we are rewriting whole thing before implementing the minimax
# According to given measures

import random


class TicTacToe:
    def __init__(self, size, computer_player=False):
        """
        Constructor for initiating the size,Board and players instance
        """
        self.size = size
        self.board = [[" "] * self.size for _ in range(self.size)]
        self.Players = {1: None, 2: None}
        self.PlayersName = {1: None, 2: None}
        self.computer_player = computer_player

    def printBoardStatus(self):
        sep = "\n" + "-" * (self.size * 4 - 3) + "\n"
        print("\n" + sep.join(" | ".join(col) for col in self.board) + "\n")

    def ChooseSymbol(self):
        """
        Most important function to randomly choose which player is gonna have
        the which symbol
        """
        symbol = ["X", "O"]
        random.shuffle(symbol)

        return symbol[0], symbol[1]

    def makeMove(self, player: int):
        if self.computer_player and player == 2:
            print("Computers Turn ")
            row, col, best_sc = self.find_best_move()

            if row == -1 and col == -1:
                print("Error in Selection by AI")

            print(f"Computer Chooses ({row + 1},{col + 1}), and  score is {best_sc}")
            return row, col

        while True:
            try:
                row = int(
                    input(f"Enter the ROW Player {player} ({self.Players[player]}) : ")
                )
                col = int(
                    input(
                        f"Enter the COLUMN Player {player} ({self.Players[player]}) : "
                    )
                )
            except ValueError as e:
                print(f"Error: {e}")
                continue
            if 1 <= row <= len(self.board) and 1 <= col <= len(self.board):
                return row - 1, col - 1

            print(f"Enter the valid Range between the 1  and {len(self.board)} ")

    def playOneRound(self, player: int) -> None:
        """
        Handle a single round of the game.
        """
        while True:
            row, col = self.makeMove(player)
            if self.board[row][col] == " ":
                self.board[row][col] = self.Players[player]

                break
            print("Space is occupied.")

    def check_winner(self):
        """
        Check for a winner based on the last move.
        """
        n = len(self.board)

        for row in range(n):
            if self.board[row][0] != " " and all(
                self.board[row][0] == self.board[row][col] for col in range(n)
            ):
                return self.board[row][0]

        # for columns
        for col in range(n):
            if self.board[0][col] != " " and all(
                self.board[0][col] == self.board[row][col] for row in range(n)
            ):
                return self.board[0][col]

        # Diagonal
        if self.board[0][0] != " " and all(
            self.board[0][0] == self.board[i][i] for i in range(n)
        ):
            return self.board[0][0]

        if self.board[0][n - 1] != " " and all(
            self.board[0][n - 1] == self.board[i][n - 1 - i] for i in range(n)
        ):
            return self.board[0][n - 1]

        return None

    def minimax(self, board, is_maximizing, depth):
        winner = self.check_winner()
        if winner == self.Players[1]:
            return 1

        elif winner == self.Players[2]:
            return -1

        elif self.draw():
            return 0

        elif depth == 0:
            # return 0
            # i dont know why we are returning the zero  because it is not helping us
            # we just reached our depth of calculation we should give result according the condition of the board
            return self.evaluate_board(board)

        if is_maximizing:
            maxeval = -float("inf")
            for row in range(self.size):
                for col in range(self.size):
                    if board[row][col] == " ":
                        board[row][col] = self.Players[2]  # computer Move
                        score = self.minimax(board, False, depth - 1)
                        # undoing the changes || BAcktracking baby
                        board[row][col] = " "
                        maxeval = max(score, maxeval)

            return maxeval

        else:
            mineval = float("inf")
            for row in range(self.size):
                for col in range(self.size):
                    if board[row][col] == " ":
                        board[row][col] = self.Players[1]
                        score = self.minimax(board, True, depth - 1)
                        # undoing the changes ||  BAcktracking BAby
                        board[row][col] = " "
                        mineval = min(score, mineval)

            return mineval

    def evaluate_board(self, board):
        # Check for immediate wins
        if self.check_winner() == self.Players[1]:  # Player 1 wins
            return 1
        elif self.check_winner() == self.Players[2]:  # Player 2 wins
            return -1

        # Initialize scores for both players
        player1_score = 0
        player2_score = 0

        # Check rows, columns, and diagonals for potential wins
        for line in self.get_all_lines(board):
            player1_count = line.count(self.Players[1])
            player2_count = line.count(self.Players[2])
            empty_count = line.count(" ")

            # Player 1 has a potential win
            if player1_count == self.size - 1 and empty_count == 1:
                player1_score += 1
            # Player 2 has a potential win
            elif player2_count == self.size - 1 and empty_count == 1:
                player2_score += 1

        # Heuristic value: Player 1's advantage minus Player 2's advantage
        return player1_score - player2_score

    def get_all_lines(self, board):
        # so basically we have  to  make  a list which  contain rows, columns  and diagonal as a list

        lisssst = []

        for i in range(self.size):
            rows = [board[i][c] for c in range(self.size)]
            lisssst.append(rows)

        for i in range(self.size):
            cols = [board[r][i] for r in range(self.size)]
            lisssst.append(cols)

        # diagonals
        lisssst.append([board[i][i] for i in range(self.size)])

        lisssst.append([board[0][self.size - 1 - i] for i in range(self.size)])

        return lisssst

    def find_best_move(self):
        best_score = -float("inf")
        best_move = (-1, -1)

        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == " ":
                    # Check if AI can win immediately
                    self.board[row][col] = self.Players[2]
                    if self.check_winner() == self.Players[2]:
                        self.board[row][col] = " "  # Undo move
                        return row, col, best_score
                    self.board[row][col] = " "  # Undo move

        # **Check if the opponent can win next turn, block that move**
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == " ":
                    self.board[row][col] = self.Players[1]
                    # If the opponent can win, block it
                    if self.check_winner() == self.Players[1]:
                        self.board[row][col] = " "  # Undo move
                        return row, col, best_score
                    self.board[row][col] = " "  # Undo move

        # **If no immediate win/block, use minimax**
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == " ":
                    self.board[row][col] = self.Players[2]  # AI move
                    # Now AI is maximizing
                    score = self.minimax(self.board, False, 5)
                    self.board[row][col] = " "  # Undo move

                    if score > best_score:
                        best_score = score
                        best_move = (row, col)

        return best_move[0], best_move[1], best_score

    def draw(self):
        """
        This is Used to check for the Draw Situation in the Game
        """
        return all(
            self.board[i][j] != " "
            for i in range(len(self.board))
            for j in range(len(self.board))
        )

    def main(self):
        """
        This main  function where all different functionality come/align and
        meet and help in working of whole process :-
        """
        self.Players[1], self.Players[2] = self.ChooseSymbol()
        self.PlayersName[1] = input("PLayer 1 Enter your name : ")

        if not self.computer_player:
            self.PlayersName[2] = input("Player 2 Enter your name : ")

        else:
            self.PlayersName[2] = "Computer"

        player = 1
        self.printBoardStatus()
        while True:
            print(
                f"{self.PlayersName[player].upper()}'s turn Symbol: {
                    self.Players[player]
                }\n"
            )
            self.playOneRound(player)
            self.printBoardStatus()
            if self.check_winner() == self.Players[player]:
                print(
                    f"Player {self.PlayersName[player]} (Symbol: {
                        self.Players[player]
                    })  Won!!!"
                )
                break

            if self.draw():
                print("Draw !!!!  ")
                break
            player = player % len(self.Players) + 1


if __name__ == "__main__":

    def play():
        print("Welcome TicTacToe Game !!!")
        while True:
            try:
                size = int(input("\nEnter the size of the board NXN : \n"))
                if size < 3:
                    print("Size must be greater than ")
                    continue
                break
            except ValueError as e:
                print(f"Error: {e}")

        computer_player = (
            input("Play against the computer? (Y/N): ").strip().upper() == "Y"
        )
        while True:
            ttt = TicTacToe(size, computer_player)
            ttt.main()

            n = input("\nWant to play Again : Y/N ").strip().upper()

            if n != "Y":
                break

    play()
