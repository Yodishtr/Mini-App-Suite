from PySide6.QtCore import Slot

from apps.rock_paper_scissors.game import Game, Move
from apps.rock_paper_scissors.views import GameView


class RockPaperScissorsApp:
    """
    This represents the GUI entry to display the game.
    It imports the game logic to allow the app to simply instantiate this
    to play the game.
    """

    def __init__(self):
        self.views = GameView()
        # setting slots for the difficulty buttons
        self.difficulty = None
        self.views.easy_difficulty_button.clicked.connect(self.difficulty_on_button_click)
        self.views.medium_difficulty_button.clicked.connect(self.difficulty_on_button_click)
        self.views.hard_difficulty_button.clicked.connect(self.difficulty_on_button_click)
        self.views.move_buttons_disabled()

        # setting slots for the move buttons
        self.views.rock_button.clicked.connect(self.move_on_button_click)
        self.views.paper_button.clicked.connect(self.move_on_button_click)
        self.views.scissor_button.clicked.connect(self.move_on_button_click)

        # game object for the game logic
        self.game = None






    @Slot
    def difficulty_on_button_click(self):
        """
        Evaluates the difficulty chosen by the player.
        """
        buttonChosen = self.sender()
        self.views.easy_difficulty_button.setEnabled(False)
        self.views.medium_difficulty_button.setEnabled(False)
        self.views.hard_difficulty_button.setEnabled(False)
        if buttonChosen == self.views.easy_difficulty_button:
            self.difficulty = "easy"
            rounds_chosen = self.views.get_rounds_chosen()
            self.game = Game(self.difficulty, rounds_chosen)
            self.views.difficulty_display.setText(self.difficulty)
            self.views.total_rounds_display.setText(rounds_chosen)
            self.views.player_score_display.setText("0")
            self.views.computer_score_display.setText("0")
            self.views.move_buttons_enabled()
            self.views.disable_difficulty_button()

        elif buttonChosen == self.views.medium_difficulty_button:
            self.difficulty = "medium"
            rounds_chosen = self.views.get_rounds_chosen()
            self.game = Game(self.difficulty, rounds_chosen)
            self.views.difficulty_display.setText(self.difficulty)
            self.views.total_rounds_display.setText(rounds_chosen)
            self.views.player_score_display.setText("0")
            self.views.computer_score_display.setText("0")
            self.views.move_buttons_enabled()
            self.views.disable_difficulty_button()

        elif buttonChosen == self.views.hard_difficulty_button:
            self.difficulty = "hard"
            rounds_chosen = self.views.get_rounds_chosen()
            self.game = Game(self.difficulty, rounds_chosen)
            self.views.difficulty_display.setText(self.difficulty)
            self.views.total_rounds_display.setText(rounds_chosen)
            self.views.player_score_display.setText("0")
            self.views.computer_score_display.setText("0")
            self.views.move_buttons_enabled()
            self.views.disable_difficulty_button()

    @Slot
    def move_on_button_click(self):
        """
        Controller uses this to determine which move has been selected by the player
        :return: str
        """
        if self.game is None:
            return

        moveChosen = self.sender()
        if moveChosen == self.views.rock_button:
            self.views.move_animation("ROCK")
            current_player_move = Move["ROCK"]
            current_result = self.game.playRound(current_player_move)
            self.views.rounds_played_display.setText(self.game.currentRound)
            self.views.player_score_display.setText(self.game.playerScore)
            self.views.computer_score_display.setText(self.game.computerScore)
            if self.game.is_over():
                self.views.enable_difficulty_buttons()
                self.views.move_buttons_disabled()

        elif moveChosen == self.views.paper_button:
            self.views.move_animation("PAPER")
            current_player_move = Move["PAPER"]
            current_result = self.game.playRound(current_player_move)
            self.views.rounds_played_display.setText(self.game.currentRound)
            self.views.player_score_display.setText(self.game.playerScore)
            self.views.computer_score_display.setText(self.game.computerScore)
            if self.game.is_over():
                self.views.enable_difficulty_buttons()
                self.views.move_buttons_disabled()

        elif moveChosen == self.views.scissor_button:
            self.views.move_animation("SCISSORS")
            current_player_move = Move["SCISSORS"]
            current_result = self.game.playRound(current_player_move)
            self.views.rounds_played_display.setText(self.game.currentRound)
            self.views.player_score_display.setText(self.game.playerScore)
            self.views.computer_score_display.setText(self.game.computerScore)
            if self.game.is_over():
                self.views.enable_difficulty_buttons()
                self.views.move_buttons_disabled()
