#  we are going to make  the game called Tic-Tac-Toe
#  Ourselve no cheating all from scratch

import random


class TicTacToe:
    def __init__(self, size):
        self.size = size
        self.board = [[" "] * self.size for _ in range(self.size)]
        self.Player = {1: None, 2: None}

    def print_board_1(self):
        for i, v in enumerate(self.board):
            print(" | ".join(v))
            if i < 2:
                print("-" * 9)

    def print_board_status(self):
        sep = "\n" + "-" * (len(self.size) * 4 - 3) + "\n"
        print("\n" + sep.join(" | ".join(col) for col in self.board) + "\n")

    def choose_symbol(self):
        """
        Most important function to randomly choose which player is gonna have
        the which symbol
        """
        p = ["X", "O"]
        player1 = random.choice(p)
        p.remove(player1)
        player2 = p[0]

        return player1, player2

    def make_move(self, player):
        """
        This function helps in  making move and same time checking if it valid
        or invalid
        """
        while True:
            try:
                ro = int(input(f"Enter the row {self.Player[player]} : "))
                co = int(input(f"Enter the column {self.Player[player]} : "))

            except ValueError as e:
                print(f"Error : {e}")

            if 1 <= ro <= len(self.board) and 1 <= co <= len(self.board):
                return ro - 1, co - 1

            print(f"Please enter the value from 1 to {len(self.board)}")

    def play_one_round(self, player):
        """
        Function for running one round in Tic-Tac-Toe game
        """
        while True:
            row, col = self.make_move(player)

            if self.board[row][col] == " ":
                self.board[row][col] = self.Player[player]
                break

            print("Space is already occupied")

    def iswin(self, player):
        """
        Function for checking does the player has won the match or not
        """
        if (
            (
                self.board[0][0] == player
                and self.board[1][1] == player
                and self.board[2][2] == player
            )
            or (
                self.board[0][2] == player
                and self.board[1][1] == player
                and self.board[2][0] == player
            )
            or (
                self.board[0][1] == player
                and self.board[1][1] == player
                and self.board[2][1] == player
            )
            or (
                self.board[0][0] == player
                and self.board[1][0] == player
                and self.board[2][0] == player
            )
            or (
                self.board[0][2] == player
                and self.board[1][2] == player
                and self.board[2][2] == player
            )
        ):
            return True

        return False

    def draw(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == " ":
                    return False

        return True

    def main(self):
        """
        This main  function where all different functionality come/align and
        meet and help in working of whole process :-
            1. we will working choosing which symbol is gonna for which one
            2. printing the print_board_status before starting the match
            3. calling play_one_round , printing updated board status
            4. Checking that player has won
            5. Plus it is important to check whether the match is drawn or not
            6. most important to rotate between the player's
        """
        self.Player[1], self.Player[2] = self.choose_symbol()
        player = 1
        self.print_board()
        while True:
            self.play_one_round(player)
            self.print_board_status()
            if self.iswin(self.Player[player]):
                print(f"Player {player}  Won!!!")
                break

            if self.draw():
                print("Draw !!!!  ")
                break
            player = player % len(self.Player) + 1


if __name__ == "__main__":
    ttt = TicTacToe()
    while True:  # added the play again feature
        ttt.main()

        n = input("\nWant to play Again : Y/N ")

        if n == "N":
            break
