"""
Implements the Game logic for the number guessing game. Allows the user to choose the
difficulty.
"""
from numpy import random


class Game():
    """Class representing the game logic for the number guessing game"""

    def __init__(self):
        """Initializes the instance attributes for scorekeeping, rounds, difficulty"""
        self.rounds = 0
        self.difficulty = None
        self.player_score = 0
        self.number_to_guess = 0
        self.player_guess = 0
        self.chances = 0

    def generated_number(self):
        """Generates a number. Number found in a certain range based on chosen difficulty"""
        if self.difficulty.lower() == "easy":
            self.easy_difficulty_chosen()
        elif self.difficulty.lower() == "medium":
            self.medium_difficulty()
        else:
            self.hard_difficulty()

    def run_round(self):
        """Runs the round game logic"""
        result = self._play_game()
        if result:
            self.player_score += 1
        self.rounds += 1

    def easy_difficulty_chosen(self):
        """Player guesses a number from 1 to 10"""
        self.chances = 5
        self.number_to_guess = random.randint(1, 10)

    def medium_difficulty_chosen(self):
        """Player guesses a number between 1 and 100 with 10 chances"""
        self.chances = 10
        self.number_to_guess = random.randint(1, 100)

    def hard_difficulty_chosen(self):
        """Player guesses a number between 1 to 1000 with 20 chances"""
        self.chances = 20
        self.number_to_guess = random.randint(1, 1000)

    def _play_game(self):
        """Plays the game"""
        self.chances -= 1
        return self.player_guess == self.number_to_guess

    def _show_number_to_guess(self):
        """Returns the number to be guessed for that round"""
        return self.number_to_guess
