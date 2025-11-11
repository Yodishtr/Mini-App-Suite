"""Class representing the game logic for the word-guessing game"""
from PySide6.QtCore import QObject, Slot

from apps.word_guessing_game.game import WordGuessingLogic, GameState, GameDifficulty, LetterState
from apps.word_guessing_game.view import WordGuesserView


class WordGuesserController(QObject):
    """The controller represents the instantiation of the game with the ui.
        It handles the game logic
    """
    def __init__(self):
        super().__init__()
        self.views = WordGuesserView()
        self.game = WordGuessingLogic()

        self.views.easy_difficulty_button.clicked.connect(self.difficulty_on_click)
        self.views.medium_difficulty_button.clicked.connect(self.difficulty_on_click)
        self.views.hard_difficulty_button.clicked.connect(self.difficulty_on_click)

        self.views.user_input.returnPressed.connect(self.submit_user_input)
        self.views.submit_button.clicked.connect(self.submit_user_input)

    @Slot(bool)
    def difficulty_on_click(self):
        """Sets the difficulty of the game"""
        button_chosen = self.sender()
        if button_chosen == self.views.easy_difficulty_button:
            self.game.game_difficulty = GameDifficulty.EASY
            self.game.random_word_pick()
            self.game.set_guess_count()
            self.views.board.setup_tiles(self.game.word_length)
        elif button_chosen == self.views.medium_difficulty_button:
            self.game.game_difficulty = GameDifficulty.MEDIUM
            self.game.random_word_pick()
            self.game.set_guess_count()
            self.views.board.setup_tiles(self.game.word_length)
        elif button_chosen == self.views.hard_difficulty_button:
            self.game.game_difficulty = GameDifficulty.HARD
            self.game.random_word_pick()
            self.game.set_guess_count()
            self.views.board.setup_tiles(self.game.word_length)

    @Slot(bool)
    def submit_user_input(self):
        """does the game logic"""
        if len(self.views.user_input.text()) == 0:
            return
        else:
            self.game.user_guess = self.views.user_input.text()
            self.game.check_user_input()
