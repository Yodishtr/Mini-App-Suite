"""
Creates the GUI for the number guessing game.
"""
import os.path

from PySide6.QtCore import QUrl
from PySide6.QtWidgets import QGridLayout, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QVBoxLayout, \
    QWidget
import yaml


class NumberGameView(QMainWindow):
    """The class representing the GUI for the number guessing app."""

    def __init__(self):
        """Initializes the view for the number game view"""
        super().__init__()
        BASE_PATH = os.path.dirname(__file__)
        self.data = self._load_yaml()

        # central widget
        central_widget = QWidget()
        central_widget.setObjectName("CENTRAL")
        self.setCentralWidget(central_widget)
        central_widget_layout = QGridLayout()
        central_widget.setLayout(central_widget_layout)

        if self.data:
            background_image = self.data["path"]["background"]
            background_image_path = os.path.join(BASE_PATH, background_image)
            background_image_url = QUrl.fromLocalFile(background_image_path).toString()
            central_widget.setStyleSheet(f"""
            QWidget#central{{
                background-image: url("{background_image_url}");
                background-repeat: no-repeat;
                background-size: cover;
                background-position: center;
            }}
            """)

        # menu with scores and chances to guess left
        menu_layout = QHBoxLayout()
        player_score_layout = QVBoxLayout()
        user_score_label_title = QLabel("Player Score: ")
        self.user_score_label = QLabel("0")
        player_score_layout.addWidget(user_score_label_title)
        player_score_layout.addWidget(self.user_score_label)

        player_chances_layout = QVBoxLayout()
        user_chances_label_title = QLabel("Chances left: ")
        self.user_chances_label = QLabel("0")
        player_chances_layout.addWidget(user_chances_label_title)
        player_chances_layout.addWidget(self.user_chances_label)

        game_difficulty_layout = QVBoxLayout()
        game_difficulty_label_title = QLabel("Difficulty: ")
        self.game_difficulty_label = QLabel("")
        game_difficulty_layout.addWidget(game_difficulty_label_title)
        game_difficulty_layout.addWidget(self.game_difficulty_label)

        menu_layout.addLayout(player_score_layout)
        menu_layout.addSpacing(20)
        menu_layout.addLayout(player_chances_layout)
        menu_layout.addSpacing(20)
        menu_layout.addLayout(game_difficulty_layout)
        menu_layout.addSpacing(20)

        # horizontal layout for the user input
        # dont forget to set the .connect methods in the app.py for the lineedit
        # self.lineedit.returnPressed.connect(self.return_pressed)
        # self.lineedit.selectionChanged.connect(self.selection_changed)
        # self.lineedit.textChanged.connect(self.text_changed)
        # self.lineedit.textEdited.connect(self.text_edited)
        user_guess_layout = QHBoxLayout()
        self.user_input_label = QLabel("Guess it!")
        self.user_input_box = QLineEdit()
        self.user_input_box.setMaxLength(10)
        self.user_input_box.setPlaceholderText("Enter your guess")
        user_guess_layout.addWidget(self.user_input_label)
        user_guess_layout.addSpacing(10)
        user_guess_layout.addWidget(self.user_input_box)
        user_guess_layout.addSpacing(5)

        # setting up the central widget
        # starts on r0 and c1, spans 2r and 6 col
        central_widget_layout.addLayout(menu_layout, 0, 1, 2, 6)
        # starts on r4 and c1, spans 2 r and 6 col
        central_widget_layout.addLayout(user_guess_layout, 4, 1, 2, 5)


    def _load_yaml(self):
        """Loads the data from the yaml"""
        try:
            with open('config.yaml', 'r') as file:
                result = yaml.safe_load(file)
                return result
        except FileNotFoundError:
            print("No config.yaml found")
            return None
        except yaml.YAMLError as e:
            print("Yaml error: " + str(e))
            return None
