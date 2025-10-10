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

        self.views.disable_guess_box()

        # setting up the difficulty buttons
        self.views.easy_difficulty_button.clicked.connect(self.difficulty_on_click)
        self.views.medium_difficulty_button.clicked.connect(self.difficulty_on_click)
        self.views.hard_difficulty_button.clicked.connect(self.difficulty_on_click)

        # set the line edit methods to poll for when return pressed or text changed
        self.views.user_input_box.returnPressed.connect(self.user_submission)
        # self.views.user_input_box.textEdited.connect(self.user_edit_guess)

        # set up play button and reset button
        self.views.play_button.clicked.connect(self.play_game_on_click)
        self.views.reset_button.clicked.connect(self.reset_game_on_click)


    @Slot
    def play_game_on_click(self):
        """
        Starts the game for guessing
        """
        self.game.current_round_score = 0
        self.views.disable_difficulty_button()
        self.views.play_button.setDisabled(True)
        self.views.enable_guess_box()


    @Slot
    def reset_game_on_click(self):
        """
        Resets the scores, difficulty and number of guesses.
        """
        self.game.reset_game()
        self.views.user_score_label.setText(str(0))
        self.views.user_chances_label.setText(str(0))
        self.views.game_difficulty_label.setText("")
        self.views.user_input_box.clear()
        self.views.user_result_label.clear()

    @Slot
    def user_submission(self):
        """
        Extracts guess made by user when pressing enter checks if it is the correct guess.
        """
        current_user_guess = self.views.user_input_box.text()
        try:
            guess = int(current_user_guess)
        except ValueError:
            self.views.user_result_label.setText("Enter a valid guess")
            return

        self.game.player_guess = guess
        current_result = self.game.run_round()
        self.views.user_chances_label.setText(str(self.game.chances))
        if current_result:
            self.views.user_score_label.setText(str(self.game.player_score))
            self.views.user_result_label.setText("You Win! Big Man Ting Ova 'Ere!")
            self.views.disable_guess_box()
            self.views.play_button.setEnabled(True)
            self.views.enable_difficulty_buttons()
        else:
            if self.game.chances > 0 and guess > self.game.number_to_guess:
                self.views.user_result_label.setText("High guess")
            elif self.game.chances > 0 and guess < self.game.number_to_guess:
                self.views.user_result_label.setText("Low Guess")
            elif self.game.chances <= 0:
                self.views.user_result_label.setText("You Lose Big Man!")
                self.views.disable_guess_box()
                self.views.play_button.setEnabled(True)
                self.views.enable_difficulty_buttons()

    # @Slot
    # def user_edit_guess(self):
    #     """
    #     Extracts the edited text made by the user and returns it to be used during the game.
    #     """
    #     return self.views.user_input_box.text()

    @Slot
    def difficulty_on_click(self):
        """
        sets the difficulty for the game
        """
        button_chosen = self.sender()
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
