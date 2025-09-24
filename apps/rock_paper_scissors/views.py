"""
Creates the specific UI for rock paper scissors.
Utilizes the common/ui/__init__ as a wrapper to keep fonts, colors and styles
consistent across the app.

"""
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QGridLayout, QMainWindow, QPushButton, QSpinBox, QVBoxLayout, QWidget


class GameView(QMainWindow):
    """A class that represents the main game window"""

    def __init__(self):
        """View Initialization"""
        super().__init__()
        self.setWindowTitle("Welcome to the Rock-Paper-Scissors Game!")
        self.setGeometry(400, 400, 800, 600)

        # Difficulty settings
        self.easy_difficulty_button = QPushButton("Easy")
        self.medium_difficulty_button = QPushButton("Medium")
        self.hard_difficulty_button = QPushButton("Hard")

        # set number of rounds
        self.roundsChosen = QSpinBox()
        self.setupRoundsChosen()

        # set moves Button
        self.rock_button = QPushButton("Rock")
        self.paper_button = QPushButton("Paper")
        self.scissor_button = QPushButton("Scissors")

        currentCentralWidget = self.create_central_widget()
        self.setCentralWidget(currentCentralWidget)

        self.setup_ui()


    def create_central_widget(self):
        """
        Creating the central widget for the main screen.
        :return: a central widget object
        """
        centralWidget = QWidget()

        # main vertical layout
        mainBoxLayout = QVBoxLayout()
        centralWidget.setLayout(mainBoxLayout)
        return centralWidget

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
            print("Player chose easy difficulty")
        elif buttonChosen == self.medium_difficulty_button:
            print("Player chose medium difficulty")
        elif buttonChosen == self.hard_difficulty_button:
            print("Player chose hard difficulty")

    def setupRoundsChosen(self):
        """
        Setting up the settings for the number of rounds chosen by the player
        """
        self.roundsChosen.setMinimum(1)
        self.roundsChosen.setMaximum(1000)
        self.roundsChosen.setSingleStep(1)
        self.roundsChosen.setSuffix("Rounds")
