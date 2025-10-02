import os
from PySide6.QtCore import QObject, Qt, Slot
from PySide6.QtGui import QPixmap

from apps.rock_paper_scissors.game import Game, Move
from apps.rock_paper_scissors.views import GameView


class RockPaperScissorsApp(QObject):
    """
    This represents the GUI entry to display the game.
    It imports the game logic to allow the app to simply instantiate this
    to play the game.
    """

    def __init__(self):
        super().__init__()
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

        # set slot for the reset button in the view
        self.views.reset_button.clicked.connect(self.reset_on_click)

    @Slot(bool)
    def reset_on_click(self, checked: bool = False):
        """
        Resets the difficulty and the game states to None
        """
        self.game.difficulty = ""
        self.game.numRounds = 0
        self.game.currentRound = 0
        self.game.computerWins = 0
        self.game.playerWins = 0
        self.game.computerScore = 0
        self.game.playerScore = 0
        self.game.computerMove = 0
        self.game.draws = 0
        self.views.move_buttons_disabled()
        self.views.enable_difficulty_buttons()

    @Slot(bool)
    def difficulty_on_button_click(self, checked: bool = False):
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
            self.views.total_rounds_display.setText(str(rounds_chosen))
            self.views.rounds_played_display.setText(str(0))
            self.views.player_score_display.setText("0")
            self.views.computer_score_display.setText("0")
            self.views.move_buttons_enabled()
            self.views.disable_difficulty_button()

        elif buttonChosen == self.views.medium_difficulty_button:
            self.difficulty = "medium"
            rounds_chosen = self.views.get_rounds_chosen()
            self.game = Game(self.difficulty, rounds_chosen)
            self.views.difficulty_display.setText(self.difficulty)
            self.views.total_rounds_display.setText(str(rounds_chosen))
            self.views.rounds_played_display.setText(str(0))
            self.views.player_score_display.setText("0")
            self.views.computer_score_display.setText("0")
            self.views.move_buttons_enabled()
            self.views.disable_difficulty_button()

        elif buttonChosen == self.views.hard_difficulty_button:
            self.difficulty = "hard"
            rounds_chosen = self.views.get_rounds_chosen()
            self.game = Game(self.difficulty, rounds_chosen)
            self.views.difficulty_display.setText(self.difficulty)
            self.views.total_rounds_display.setText(str(rounds_chosen))
            self.views.rounds_played_display.setText(str(0))
            self.views.player_score_display.setText("0")
            self.views.computer_score_display.setText("0")
            self.views.move_buttons_enabled()
            self.views.disable_difficulty_button()

    @Slot(bool)
    def move_on_button_click(self, checked: bool = False):
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

            computer_move = self.game.computerMove
            self.add_computer_move_image(computer_move)

            self.views.rounds_played_display.setText(str(self.game.currentRound))
            self.views.player_score_display.setText(str(self.game.playerScore))
            self.views.computer_score_display.setText(str(self.game.computerScore))
            if self.game.is_over():
                self.views.enable_difficulty_buttons()
                self.views.move_buttons_disabled()
                if self.game.playerScore > self.game.computerScore:
                    self.views.result_label_display.setText("Player Won")
                elif self.game.playerScore < self.game.computerScore:
                    self.views.result_label_display.setText("Computer Won")
                elif (self.game.draws > self.game.computerScore and
                      self.game.draws > self.game.computerScore):
                    self.views.result_label_display.setText("Draw")

        elif moveChosen == self.views.paper_button:
            self.views.move_animation("PAPER")
            current_player_move = Move["PAPER"]
            current_result = self.game.playRound(current_player_move)

            computer_move = self.game.computerMove
            self.add_computer_move_image(computer_move)

            self.views.rounds_played_display.setText(str(self.game.currentRound))
            self.views.player_score_display.setText(str(self.game.playerScore))
            self.views.computer_score_display.setText(str(self.game.computerScore))
            if self.game.is_over():
                self.views.enable_difficulty_buttons()
                self.views.move_buttons_disabled()
                if self.game.playerScore > self.game.computerScore:
                    self.views.result_label_display.setText("Player Won")
                elif self.game.playerScore < self.game.computerScore:
                    self.views.result_label_display.setText("Computer Won")
                elif (self.game.draws > self.game.computerScore and
                      self.game.draws > self.game.computerScore):
                    self.views.result_label_display.setText("Draw")

        elif moveChosen == self.views.scissor_button:
            self.views.move_animation("SCISSORS")
            current_player_move = Move["SCISSORS"]
            current_result = self.game.playRound(current_player_move)

            computer_move = self.game.computerMove
            self.add_computer_move_image(computer_move)

            self.views.rounds_played_display.setText(str(self.game.currentRound))
            self.views.player_score_display.setText(str(self.game.playerScore))
            self.views.computer_score_display.setText(str(self.game.computerScore))
            if self.game.is_over():
                self.views.enable_difficulty_buttons()
                self.views.move_buttons_disabled()
                if self.game.playerScore > self.game.computerScore:
                    self.views.result_label_display.setText("Player Won")
                elif self.game.playerScore < self.game.computerScore:
                    self.views.result_label_display.setText("Computer Won")
                elif (self.game.draws > self.game.computerScore and
                      self.game.draws > self.game.computerScore):
                    self.views.result_label_display.setText("Draw")

    def add_computer_move_image(self, computer_move):
        """
        Displays the computer's move in the gui
        :param computer_move:
        """
        BASE_PATH = os.path.dirname(__file__)
        if computer_move.value == "rock":
            rock_image = os.path.join(BASE_PATH, "hand.png")
            rock_pixmap = QPixmap(rock_image)
            scaled_rock_pixmap = rock_pixmap.scaled(
                self.views.computer_move_label_image.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.views.computer_move_label_image.setPixmap(scaled_rock_pixmap)
        elif computer_move.value == "paper":
            paper_image = os.path.join(BASE_PATH, "hand-paper.png")
            paper_pixmap = QPixmap(paper_image)
            scaled_paper_pixmap = paper_pixmap.scaled(
                self.views.computer_move_label_image.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.views.computer_move_label_image.setPixmap(scaled_paper_pixmap)
        else:
            scissors_image = os.path.join(BASE_PATH, "scissors.png")
            scissors_pixmap = QPixmap(scissors_image)
            scaled_scissor_pixmap = scissors_pixmap.scaled(
                self.views.computer_move_label_image.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.views.computer_move_label_image.setPixmap(scaled_scissor_pixmap)


if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    rps_app = RockPaperScissorsApp()
    rps_app.views.show()
    sys.exit(app.exec())
