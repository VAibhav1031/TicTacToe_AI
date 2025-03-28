#  we are going to make  the game called Tic-Tac-Toe
#  Ourselve no cheating all from scratch

import random


class TicTacToe:
    def __init__(self):
        self.board = [[" "] * 3 for _ in range(3)]
        self.Player = {1: None, 2: None}

    def print_board(self):
        for i in range(3):
            print(f"{self.board[i][0]}  | {
                  self.board[i][1]} | {self.board[i][2]}")

            if i < 2:
                print("-" * 11)

    def print_board_1(self):
        for i, v in enumerate(self.board):
            print(" | ".join(v))
            if i < 2:
                print("-" * 9)

    def print_board_status(self):
        sep = "\n" + "-" * (len(self.board) * 4 - 3) + "\n"
        print("\n" + sep.join(" | ".join(col) for col in self.board) + "\n")

    def choose_symbol(self):
        p = ["X", "O"]
        player1 = random.choice(p)
        p.remove(player1)
        player2 = p[0]

        return player1, player2

    def make_move(self, player):
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
        while True:
            row, col = self.make_move(player)

            if self.board[row][col] == " ":
                self.board[row][col] = self.Player[player]
                break

            print("Space is already occupied")

    def iswin(self, player):
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

        computer_player = (
            input("Play against the computer? (Y/N): ").strip().upper() == "Y"
        )

        while True:
            ttt = TicTacToe(size, computer_player)
            ttt.main()
            n = input("\nWant to play again? (Y/N): ").strip().upper()
            if n != "Y":
                break

    play()
