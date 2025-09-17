from enum import Enum
"""
This contains the pure logic of the game such as the current state and
the game rules etc.

"""


"""This is an inner class to represent the move of a player"""
class Move(Enum):
    ROCK = "rock"
    PAPER = "paper"
    SCISSORS = "scissors"

    def beats(self, other):
        """Checks the winning move from the two inputs"""
        if self == Move.ROCK and other == Move.SCISSORS:
            return True
        elif self == Move.SCISSORS and other == Move.PAPER:
            return True
        elif self == Move.PAPER and other == Move.ROCK:
            return True
        else:
            return False


"""This class represents the game logic for rock paper scissors"""

class Game:
    def __init__(self, difficulty: str, num_round=5):
        self.difficulty = difficulty
        self.rounds = num_round
