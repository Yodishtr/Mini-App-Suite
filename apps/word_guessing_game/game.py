"""A class representing the game logic for the word guessing game."""
import os.path
from enum import Enum
from apps.word_guessing_game.filereader import WordProvider


class LetterState(Enum):
    """a state machine to determine the way the letters input by the user"""
    CORRECT = "GREEN"
    PRESENT = "YELLOW"
    ABSENT = "RED"
    UNKNOWN = "GREY"


class GameDifficulty(Enum):
    """a state machine to determine the game difficulty chosen by the user"""
    EASY = 1
    MEDIUM = 2
    HARD = 3


class GameState(Enum):
    """a state machine to determine the current game state"""
    RUNNING = 1
    WIN = 2
    LOSE = 3


class WordGuessingLogic():
    """Class representing the game logic for the word guessing games"""
    def __init__(self):
        """game logic constructor for the word guessing game."""
        self.word_target = None
        self.game_difficulty = None
        self.guess_count = None
        self.user_guess = None
        self.game_state = GameState.RUNNING

        # initialized and store the word provider object
        BASE_PATH = os.path.dirname(__file__)
        EASY_FILE = "easy.txt"
        MEDIUM_FILE = "medium.txt"
        HARD_FILE = "hard.txt"
        easy_file_path = os.path.join(BASE_PATH, EASY_FILE)
        medium_file_path = os.path.join(BASE_PATH, MEDIUM_FILE)
        hard_file_path = os.path.join(BASE_PATH, HARD_FILE)
        self.word_provider = WordProvider(easy_file_path, medium_file_path, hard_file_path)
        self.word_provider.load_easy_words()
        self.word_provider.load_medium_words()
        self.word_provider.load_hard_words()

    def random_word_pick(self):
        """chooses the random word based on the game difficulty chosen by the user"""
        if self.game_difficulty == GameDifficulty.EASY:
            self.easy_pick()
        elif self.game_difficulty == GameDifficulty.MEDIUM:
            pass
        else:
            pass

    def easy_pick(self):
        """Chooses a random easy word from the easy word list in word provider"""
        pass
