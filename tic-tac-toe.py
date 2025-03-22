##################
# Bit improvement
#################


# you know  we have already the imrovement measures,we are rewriting whole thing before implementing the minimax
# According to given measures

import random


class TicTacToe:
    def __init__(self, size):
        """
        Constructor for initiating the size,Board and players instance
        """
        self.size = size
        self.board = [[" "] * self.size for _ in range(self.size)]
        self.Players = {1: None, 2: None}
        self.PlayersName = {1: None, 2: None}

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
        Help in running Single Round
        """
        while True:
            row, col = self.makeMove(player)

            if self.board[row][col] == " ":
                self.board[row][col] = self.Players[player]
                break

            print("Space is ocuupied ")

    def isWin(self, player: int) -> bool:
        """
        function To check does this player have won or not
        """
        # rows
        n = len(self.board)
        for row in range(n):
            if all(self.board[row][col] == self.Players[player] for col in range(n)):
                return True

        # columns
        for col in range(n):
            if all(self.board[row][col] == self.Players[player] for row in range(n)):
                return True

        # diagonals
        if all(self.board[i][i] == self.Players[player] for i in range(n)):
            return True

        if all(
            self.board[i][len(self.board) - 1 - i] == self.Players[player]
            for i in range(n)
        ):
            return True
        return False

    def draw(self):
        """
        This is Used to check for the Draw Situation in the Game
        """
        # for i in range(len(self.board)):
        #     for j in range(len(self.board)):
        #         if self.board[i][j] == " ":
        #             return False
        #
        # return True
        #
        #

        return all(
            self.board[i][j] != " "
            for i in range(len(self.board))
            for j in range(len(self.board))
        )

    def main(self):
        """
        This main  function where all different functionality come/align and
        meet and help in working of whole process :-
            1. we will working choosing which symbol is gonna for which one
            2. printing the print_board_status before starting the match
            3. calling play_one_round , printing updated board status
            4. Checking that player has won
            5. Plus Nit is important to check whether the match is drawn or not
            6. most important to rotate between the player's
        """
        self.Players[1], self.Players[2] = self.ChooseSymbol()
        self.PlayersName[1] = input("PLayer 1 Enter your name : ")
        self.PlayersName[2] = input("Player 2 Enter your name : ")

        player = 1
        self.printBoardStatus()
        while True:
            print(
                f"{self.PlayersName[player].upper()}'s turn Symbol: {self.Players[1]}\n"
            )
            self.playOneRound(player)
            self.printBoardStatus()
            if self.isWin(player):
                print(f"Player {player} (Symbol: {self.Players[player]})  Won!!!")
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

        while True:
            ttt = TicTacToe(size)
            ttt.main()

            n = input("\nWant to play Again : Y/N ").strip().upper()

            if n != "Y":
                break

    play()
