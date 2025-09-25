"""
Creates the specific UI for rock paper scissors.
Utilizes the common/ui/__init__ as a wrapper to keep fonts, colors and styles
consistent across the app.

"""
import os.path
from pathlib import Path

from PySide6.QtCore import Slot
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QGridLayout, QHBoxLayout, QLabel, QMainWindow, QPushButton, QSpinBox, \
    QVBoxLayout, QWidget


class GameView(QMainWindow):
    """A class that represents the main game window"""

    def __init__(self):
        """View Initialization"""
        super().__init__()
        self.setWindowTitle("Welcome to the Rock-Paper-Scissors Game!")
        self.setGeometry(400, 400, 800, 600)

        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_layout = QGridLayout(central_widget)

        # Difficulty settings
        self.easy_difficulty_button = QPushButton("Easy")
        self.medium_difficulty_button = QPushButton("Medium")
        self.hard_difficulty_button = QPushButton("Hard")

        # set number of rounds
        self.roundsChosen = QSpinBox()
        self.setupRoundsChosen()

        # Set moves Button
        # dont forget to create its own layout to be added to the central layout
        # use a QHBoxLayout for this and also add the .connect.clicked method
        moves_layout = QHBoxLayout()
        self.rock_button = QPushButton("Rock")
        self.paper_button = QPushButton("Paper")
        self.scissor_button = QPushButton("Scissors")
        # add icons to the moves button
        BASE_PATH = os.path.dirname(__file__)
        rock_icon = os.path.join(BASE_PATH, "hand.png")
        self.rock_button.setIcon(QIcon(rock_icon))
        self.rock_button.clicked.connect(self.move_on_button_click)

        paper_icon = os.path.join(BASE_PATH, "hand-paper.png")
        self.paper_button.setIcon(QIcon(paper_icon))
        self.paper_button.clicked.connect(self.move_on_button_click)

        scissors_icon = os.path.join(BASE_PATH, "scissors.png")
        self.scissor_button.setIcon(QIcon(scissors_icon))
        self.scissor_button.clicked.connect(self.move_on_button_click)

        # Menu Labels
        menu_layout = QHBoxLayout()

        difficulty_layout = QVBoxLayout()
        difficulty_title = QLabel("Difficulty")
        self.difficulty_display = QLabel("")
        difficulty_layout.addWidget(difficulty_title)
        difficulty_layout.addWidget(self.difficulty_display)

        total_rounds_layout = QVBoxLayout()
        total_rounds_title = QLabel("Total rounds")
        self.total_rounds_display = QLabel()
        total_rounds_layout.addWidget(total_rounds_title)
        total_rounds_layout.addWidget(self.total_rounds_display)

        rounds_played_layout = QVBoxLayout()
        rounds_played_title = QLabel("Rounds Played: ")
        self.rounds_played_display = QLabel()
        rounds_played_layout.addWidget(rounds_played_title)
        rounds_played_layout.addWidget(self.rounds_played_display)

        player_score_layout = QVBoxLayout()
        player_score_title = QLabel("Player Score")
        self.player_score_display = QLabel()
        player_score_layout.addWidget(player_score_title)
        player_score_layout.addWidget(self.player_score_display)

        computer_score_layout = QVBoxLayout()
        computer_score_title = QLabel("Computer Score")
        self.computer_score_display = QLabel()
        computer_score_layout.addWidget(computer_score_title)
        computer_score_layout.addWidget(self.computer_score_display)

        menu_layout.addLayout(difficulty_layout)
        menu_layout.addSpacing(20)
        menu_layout.addLayout(total_rounds_layout)
        menu_layout.addSpacing(20)
        menu_layout.addLayout(rounds_played_layout)
        menu_layout.addSpacing(20)
        menu_layout.addLayout(player_score_layout)
        menu_layout.addSpacing(20)
        menu_layout.addLayout(computer_score_layout)

        # Central layout adding other layouts
        central_layout.addLayout(menu_layout, 0, 0, 2, 5)

        self.setup_ui()

    def setup_ui(self):
        """
        Sets up the UI for the main focus of the game.
        """
        ui_setup_widget = QWidget()
        ui_setup_layout = QGridLayout()
        ui_setup_widget.setLayout(ui_setup_layout)

        self.easy_difficulty_button.clicked.connect(self.difficulty_on_button_click)
        self.medium_difficulty_button.clicked.connect(self.difficulty_on_button_click)
        self.hard_difficulty_button.clicked.connect(self.difficulty_on_button_click)

        self.setupRoundsChosen()

    @Slot
    def difficulty_on_button_click(self):
        """
        Evaluates the difficulty chosen by the player.
        """
        buttonChosen = self.sender()
        if buttonChosen == self.easy_difficulty_button:
            return ("easy")
        elif buttonChosen == self.medium_difficulty_button:
            return ("medium")
        elif buttonChosen == self.hard_difficulty_button:
            return ("hard")

    @Slot
    def move_on_button_click(self):
        """
        Controller uses this to determine which move has been selected by the player
        :return: str
        """
        moveChosen = self.sender()
        if moveChosen == self.rock_button:
            return ("ROCK")
        elif moveChosen == self.paper_button:
            return ("PAPER")
        elif moveChosen == self.scissor_button:
            return ("SCISSORS")

    def setupRoundsChosen(self):
        """
        Setting up the settings for the number of rounds chosen by the player
        """
        self.roundsChosen.setMinimum(1)
        self.roundsChosen.setMaximum(1000)
        self.roundsChosen.setSingleStep(1)
        self.roundsChosen.setSuffix("Rounds")

    def update_difficulty(self, level: str):
        """
        Controller uses this to update the difficulty set by the player
        :param level:
        """
        self.difficulty_display.setText(level)

    def update_total_rounds(self, total_rounds):
        """
        Controller uses this to update the total number of rounds selected by the player
        :param total_rounds:
        """
        self.total_rounds_display.setText(total_rounds)

    def update_rounds_played(self, played: str):
        """
        Controller uses this to update the  rounds played till now in the game.
        :param played:
        """
        self.rounds_played_display.setText(played)

    def update_player_score(self, player_score: str):
        """
        Controller uses this to update the score board with the player's current score
        :param player_score:
        """
        self.player_score_display.setText(player_score)

    def update_computer_score(self, computer_score: str):
        """
        Controller uses this to update the score board with the computer's current score
        :param computer_score:
        """
        self.computer_score_display.setText(computer_score)
