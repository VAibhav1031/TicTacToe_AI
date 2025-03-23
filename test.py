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
        self.memo = {}

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

    def makeMove(self, player: int, board):
        if self.computer_player and player == 2:
            print("Computers Turn ")
            row, col, best_sc = self.find_best_move(board)

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

    def playOneRound(self, player: int, board) -> None:
        """
        Handle a single round of the game.
        """
        while True:
            row, col = self.makeMove(player, board)
            if self.board[row][col] == " ":
                self.board[row][col] = self.Players[player]

                break
            print("Space is occupied.")

    def check_winner(self, board):
        """
        Check for a winner based on the last move.
        """
        n = len(board)

        for row in range(n):
            if board[row][0] != " " and all(
                board[row][0] == board[row][col] for col in range(n)
            ):
                return board[row][0]

        # for columns
        for col in range(n):
            if board[0][col] != " " and all(
                board[0][col] == board[row][col] for row in range(n)
            ):
                return board[0][col]

        # Diagonal
        if board[0][0] != " " and all(board[0][0] == board[i][i] for i in range(n)):
            return board[0][0]

        if board[0][n - 1] != " " and all(
            board[0][n - 1] == board[i][n - 1 - i] for i in range(n)
        ):
            return board[0][n - 1]

        return None

    def minimax(
        self, board, is_maximizing, depth=None, alpha=-float("inf"), beta=float("inf")
    ):
        if depth is None:
            depth = min(6, len([cell for row in board for cell in row if cell == " "]))

        # Convert board to tuple for hashing
        board_key = tuple(tuple(row) for row in board)
        if board_key in self.memo:
            return self.memo[board_key]

        winner = self.check_winner(board)
        if winner == self.Players[1]:
            return 100 + depth

        elif winner == self.Players[2]:
            return -100 - depth

        elif self.draw(board) or depth == 0:
            return self.evaluate_board(board)

        if is_maximizing:
            maxeval = -float("inf")
            for row in range(self.size):
                for col in range(self.size):
                    if board[row][col] == " ":
                        tmp_board = [list(row) for row in board]
                        tmp_board[row][col] = self.Players[2]  # computer Move
                        score = self.minimax(tmp_board, False, depth - 1)

                        maxeval = max(score, maxeval)
                        alpha = max(alpha, maxeval)
                        if beta <= alpha:
                            break
            self.memo[board_key] = maxeval
            return maxeval

        else:
            mineval = float("inf")
            for row in range(self.size):
                for col in range(self.size):
                    if board[row][col] == " ":
                        tmp_board = [list(row) for row in board]
                        tmp_board[row][col] = self.Players[1]
                        score = self.minimax(tmp_board, True, depth - 1)

                        mineval = min(score, mineval)
                        beta = min(beta, mineval)
                        if beta <= alpha:
                            break

            self.memo[board_key] = mineval
            return mineval

    def evaluate_board(self, board):
        score = 0

        # Check rows, columns, and diagonals
        for i in range(self.size):
            score += self.evaluate_line([board[i][j] for j in range(self.size)])  # Row
            score += self.evaluate_line(
                [board[j][i] for j in range(self.size)]
            )  # Column

        score += self.evaluate_line(
            [
                board[i][i]
                # Main diagonal
                for i in range(self.size)
            ]
        )
        score += self.evaluate_line(
            [
                board[i][self.size - i - 1]
                # Anti-diagonal
                for i in range(self.size)
            ]
        )

        return score

    def evaluate_line(self, line):
        """Assigns scores based on how strong a row/col/diagonal is."""
        ai_count = line.count(self.Players[2])  # AI's symbol
        human_count = line.count(self.Players[1])  # Player's symbol

        if ai_count > 0 and human_count == 0:
            return 10**ai_count  # AI advantage
        elif human_count > 0 and ai_count == 0:
            return -(10**human_count)  # Player advantage
        return 0  # Neutral

    # def evaluate_board(self, board):
    #     # Check for immediate wins
    #     if self.check_winner(board) == self.Players[1]:  # Player 1 wins
    #         return 100
    #     elif self.check_winner(board) == self.Players[2]:  # Player 2 wins
    #         return -100
    #
    #     # Initialize scores for both players
    #     player1_score = 0
    #     player2_score = 0
    #
    #     # Check rows, columns, and diagonals for potential wins
    #     for line in self.get_all_lines(board):
    #         player1_count = line.count(self.Players[1])
    #         player2_count = line.count(self.Players[2])
    #         empty_count = line.count(" ")
    #
    #         # Player 1 has a potential win
    #         if player1_count == self.size - 1 and empty_count == 1:
    #             player1_score += 10
    #         # Player 2 has a potential win
    #         elif player2_count == self.size - 1 and empty_count == 1:
    #             player2_score += 10
    #
    #         elif player1_count == self.size - 2 and empty_count == 2:
    #             player1_score += 3
    #
    #         elif player2_count == self.size - 2 and empty_count == 2:
    #             player2_score += 3
    #
    #     # Heuristic value: Player 1's advantage minus Player 2's advantage
    #     return player1_score - player2_score

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

    def find_best_move(self, board):
        best_score = -float("inf")
        best_move = (-1, -1)

        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == " ":
                    # Check if AI can win immediately
                    tmp_board = [list(row) for row in board]
                    tmp_board[row][col] = self.Players[2]
                    if self.check_winner(tmp_board) == self.Players[2]:
                        return row, col, 100

        # **Check if the opponent can win next turn, block that move**
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == " ":
                    tmp_board = [list(row) for row in board]
                    tmp_board[row][col] = self.Players[1]
                    # If the opponent can win, block it
                    if self.check_winner(tmp_board) == self.Players[1]:
                        return row, col, 50

        # **If no immediate win/block, use minimax**
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == " ":
                    tmp_board = [list(row) for row in board]
                    tmp_board[row][col] = self.Players[2]  # AI move
                    # Now AI is maximizing
                    score = self.minimax(tmp_board, False, 5)
                    if score > best_score:
                        best_score = score
                        best_move = (row, col)

        return best_move[0], best_move[1], best_score

    def draw(self, board):
        """
        This is Used to check for the Draw Situation in the Game
        """
        return all(
            self.board[i][j] != " "
            for i in range(len(board))
            for j in range(len(board))
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
            self.playOneRound(player, self.board)
            self.printBoardStatus()
            if self.check_winner(self.board) == self.Players[player]:
                print(
                    f"Player {self.PlayersName[player].upper()} (Symbol: {
                        self.Players[player]
                    })  Won!!!"
                )
                break

            if self.draw(self.board):
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
                    print("Size must be greater than 3")
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
