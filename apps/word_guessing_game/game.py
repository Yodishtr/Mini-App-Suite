"""A class representing the game logic for the word guessing game."""
import os.path
from enum import Enum
from random import randint

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
        self.word_length = 0
        self.game_difficulty = None
        self.guess_count = None
        self.user_guess = None
        self.game_state = GameState.RUNNING
        self.guess_result = []
        self.guess_result_correct = []

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
            self.medium_pick()
        else:
            self.hard_pick()

    def easy_pick(self):
        """Chooses a random easy word from the easy word list in word provider"""
        random_idx = randint(0, self.word_provider.easy_count)
        random_word = self.word_provider.easy_lst[random_idx]
        self.word_target = random_word
        self.word_length = len(random_word)

    def hard_pick(self):
        """
        Chooses a random hard word from the hard word list in word provider
        """
        random_idx = randint(0, self.word_provider.hard_count)
        random_word = self.word_provider.hard_lst[random_idx]
        self.word_target = random_word
        self.word_length = len(random_word)

    def medium_pick(self):
        """
        Chooses a random medium word from the medium word list in word provider
        """
        random_idx = randint(0, self.word_provider.medium_count)
        random_word = self.word_provider.medium_lst[random_idx]
        self.word_target = random_word
        self.word_length = len(random_word)

    def set_guess_count(self):
        """Sets the guesses allowed by the user based on the difficulty they chose"""
        if (self.game_difficulty == GameDifficulty.EASY or
                self.game_difficulty == GameDifficulty.HARD):
            self.guess_count = 10
        else:
            self.guess_count = 12

    def check_user_input(self):
        """Checks the user input against the target word"""
        if self.user_guess is None:
            self.word_compare()
        elif self.guess_count > 1:
            self.word_compare()
            self.guess_count -= 1
        elif self.guess_count == 1:
            self.word_compare()
            if self.game_state == GameState.RUNNING:
                self.game_state = GameState.LOSE
            self.guess_count -= 1

    def word_compare(self):
        """
        processes the word comparison between the user's guess and the target word
        """
        if self.user_guess is None:
            return
        target_work_breakdown = list(self.word_target)
        user_guess_breakdown = list(self.user_guess)
        for i in range(len(user_guess_breakdown)):
            present = False
            correct = False
            for j in range(len(target_work_breakdown)):
                if user_guess_breakdown[i] == target_work_breakdown[j] and i == j:
                    correct = True
                    present = True
                    break
                elif user_guess_breakdown[i] == target_work_breakdown[j]:
                    present = True
                    break
            if correct and present:
                self.guess_result.append((user_guess_breakdown[i], i, LetterState.CORRECT))
                self.guess_result_correct.append((user_guess_breakdown[i], i, LetterState.CORRECT))
            elif not correct and present:
                self.guess_result.append((user_guess_breakdown[i], i, LetterState.PRESENT))
            elif not correct and not present:
                self.guess_result.append((user_guess_breakdown[i], i, LetterState.ABSENT))

        if len(self.guess_result_correct) == len(target_work_breakdown):
            self.game_state = GameState.WIN
