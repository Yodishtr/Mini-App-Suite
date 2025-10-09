from PySide6.QtCore import QObject, Slot

from apps.number_guessing_game.game import Game
from apps.number_guessing_game.views import NumberGameView


class NumberGuessingApp(QObject):
    """
    This represents the GUI entry to display the game.
    It imports the game logic to allow the app to simply instantiate this
    to play the game.
    """
    def __init__(self):
        super().__init__()
        self.views = NumberGameView()
        self.game = Game()

        # setting up the difficulty buttons
        self.views.easy_difficulty_button.clicked.connect(self.difficulty_on_click)
        self.views.medium_difficulty_button.clicked.connect(self.difficulty_on_click)
        self.views.hard_difficulty_button.clicked.connect(self.difficulty_on_click)

    @Slot
    def difficulty_on_click(self):
        """
        sets the difficulty for the game
        """
        button_chosen = self.sender()
        self.views.easy_difficulty_button.setEnabled(False)
        self.views.medium_difficulty_button.setEnabled(False)
        self.views.hard_difficulty_button.setEnabled(False)
        if button_chosen == self.views.easy_difficulty_button:
            self.game.difficulty = "easy"
            self.game.easy_difficulty_chosen()
            self.views.game_difficulty_label.setText("Easy")
            self.views.user_chances_label.setText(str(self.game.chances))
        elif button_chosen == self.views.medium_difficulty_button:
            self.game.difficulty = "medium"
            self.game.medium_difficulty_chosen()
            self.views.game_difficulty_label.setText("Medium")
            self.views.user_chances_label.setText(str(self.game.chances))
        elif button_chosen == self.views.hard_difficulty_button:
            self.game.difficulty = "hard"
            self.game.hard_difficulty_chosen()
            self.views.game_difficulty_label.setText("Hard")
            self.views.user_chances_label.setText(str(self.game.chances))
