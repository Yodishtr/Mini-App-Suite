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
        # self.views.restart_button.clicked.connect(self.restart_game)

    @Slot(bool)
    def difficulty_on_click(self):
        """Sets the difficulty of the game"""
        button_chosen = self.sender()
        if button_chosen == self.views.easy_difficulty_button:
            self.game.game_difficulty = GameDifficulty.EASY
            self.game.random_word_pick()
            self.game.set_guess_count()
            self.views.guess_count.setText(str(self.game.guess_count))
            self.views.board.setup_tiles(self.game.word_length)
        elif button_chosen == self.views.medium_difficulty_button:
            self.game.game_difficulty = GameDifficulty.MEDIUM
            self.game.random_word_pick()
            self.game.set_guess_count()
            self.views.guess_count.setText(str(self.game.guess_count))
            self.views.board.setup_tiles(self.game.word_length)
        elif button_chosen == self.views.hard_difficulty_button:
            self.game.game_difficulty = GameDifficulty.HARD
            self.game.random_word_pick()
            self.game.set_guess_count()
            self.views.guess_count.setText(str(self.game.guess_count))
            self.views.board.setup_tiles(self.game.word_length)
        self.views.easy_difficulty_button.setDisabled(True)
        self.views.medium_difficulty_button.setDisabled(True)
        self.views.hard_difficulty_button.setDisabled(True)
        self.views.submit_button.setDisabled(True)
        self.views.submit_button.setEnabled(True)

    @Slot(bool)
    def submit_user_input(self):
        """does the game logic"""
        self.views.board.clear_all()
        if len(self.views.user_input.text()) == 0:
            return
        else:
            self.game.user_guess = self.views.user_input.text()
            self.game.check_user_input()
            if self.game.game_state == GameState.LOSE:
                self.views.easy_difficulty_button.setEnabled(True)
                self.views.medium_difficulty_button.setEnabled(True)
                self.views.hard_difficulty_button.setEnabled(True)
                self.views.submit_button.setDisabled(True)
                self.views.board.set_text(self.game.word_target)
                self.views.game_result.setText("you lose!")
                return
            elif self.game.game_state == GameState.WIN:
                self.views.easy_difficulty_button.setEnabled(True)
                self.views.medium_difficulty_button.setEnabled(True)
                self.views.hard_difficulty_button.setEnabled(True)
                self.views.submit_button.setDisabled(True)
                self.views.game_result.setText("you win!")
                return

            self.views.board.set_text(self.game.user_guess)
            states = []
            for tup in self.game.guess_result:
                status = tup[2]
                if status == LetterState.CORRECT:
                    status = "correct"
                elif status == LetterState.PRESENT:
                    status = "present"
                else:
                    status = "absent"
                states.append(status)
            self.views.board.reveal_state(states)
            self.views.guess_count.setText(str(self.game.guess_count))
            self.game.guess_result.clear()
            self.game.guess_result_correct.clear()
