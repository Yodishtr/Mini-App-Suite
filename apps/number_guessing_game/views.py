"""
Creates the GUI for the number guessing game.
"""
import os.path

from PySide6.QtCore import Qt, QUrl

from PySide6.QtWidgets import QGridLayout, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QPushButton, \
    QVBoxLayout, \
    QWidget
import yaml
from PySide6.QtGui import QImageReader, QImage, QPixmap
import os


class NumberGameView(QMainWindow):
    """The class representing the GUI for the number guessing app."""

    def __init__(self):
        """Initializes the view for the number game view"""
        super().__init__()
        BASE_PATH = os.path.dirname(__file__)
        self.data = self._load_yaml()

        # central widget
        central_widget = QWidget()
        central_widget.setObjectName("central")
        self.setCentralWidget(central_widget)
        central_widget_layout = QGridLayout()
        central_widget.setLayout(central_widget_layout)
        central_widget.setAttribute(Qt.WA_StyledBackground, True)

        if self.data:
            background_image = self.data["path"]["background"]
            print(background_image)
            background_image_path = os.path.join(BASE_PATH, background_image)
            print(background_image_path)
            background_image_url = QUrl.fromLocalFile(background_image_path).toString()
            print(background_image_url)
            central_widget.setStyleSheet(f"""
            #central {{
                border-image: url("{background_image_path}") 0 0 0 0 stretch stretch;
            }}
            QHBoxLayout#result{{
                border: 1px dashed;
                font-size: 10px;
                font-weight: 700;
            }}
            QPushButton:hover{{
                background-color: #f0f0f0;
            }}
            QPushButton:pressed{{
                background-color: #d0d0d0;
            }}
            """)
            print("File exists:", os.path.exists(background_image))

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

        # result for being able to guess correctly or not
        user_result_layout = QHBoxLayout()
        user_result_layout.setObjectName("result")
        user_result_title = QLabel("Result: ")
        self.user_result_label = QLabel("")
        user_result_layout.addWidget(user_result_title)
        user_result_layout.addSpacing(10)
        user_result_layout.addWidget(self.user_result_label)

        # add the difficulty buttons
        difficulty_choice_layout = QHBoxLayout()
        self.easy_difficulty_button = QPushButton("Easy")
        self.medium_difficulty_button = QPushButton("Medium")
        self.hard_difficulty_button = QPushButton("Hard")
        self.play_button = QPushButton("Play")
        self.reset_button = QPushButton("Reset")
        difficulty_choice_layout.addWidget(self.easy_difficulty_button)
        difficulty_choice_layout.addSpacing(10)
        difficulty_choice_layout.addWidget(self.medium_difficulty_button)
        difficulty_choice_layout.addSpacing(10)
        difficulty_choice_layout.addWidget(self.hard_difficulty_button)
        difficulty_choice_layout.addSpacing(10)
        difficulty_choice_layout.addWidget(self.play_button)
        difficulty_choice_layout.addSpacing(10)
        difficulty_choice_layout.addWidget(self.reset_button)

        # setting up the central widget
        # starts on r0 and c1, spans 2r and 6 col
        central_widget_layout.addLayout(menu_layout, 0, 1, 2, 6)
        # starts on r3 and c1, spans 1r and 6 col
        central_widget_layout.addLayout(difficulty_choice_layout, 3, 1, 1, 6)
        # starts on r4 and c1, spans 2 r and 6 col
        central_widget_layout.addLayout(user_guess_layout, 5, 1, 2, 5)
        # starts on r8 and c1, spans 2r and 6 col
        central_widget_layout.addLayout(user_result_layout, 8, 1, 2, 6)


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

    def enable_difficulty_buttons(self):
        """
        Enables difficulty buttons if they are disabled
        """
        if (not self.easy_difficulty_button.isEnabled()
                and not self.medium_difficulty_button.isEnabled()
                and not self.hard_difficulty_button.isEnabled()):
            self.easy_difficulty_button.setEnabled(True)
            self.medium_difficulty_button.setEnabled(True)
            self.hard_difficulty_button.setEnabled(True)

    def disable_difficulty_button(self):
        """
        Disables difficulty buttons if they are enabled
        """
        if (self.easy_difficulty_button.isEnabled()
                and self.medium_difficulty_button.isEnabled()
                and self.hard_difficulty_button.isEnabled()):
            self.easy_difficulty_button.setEnabled(False)
            self.medium_difficulty_button.setEnabled(False)
            self.hard_difficulty_button.setEnabled(False)

    def enable_guess_box(self):
        """
        Enables the guess box, ie line edit widget, if disabled
        """
        if (not self.user_input_box.isEnabled()):
            self.user_input_box.setEnabled(True)

    def disable_guess_box(self):
        """
        Disables the guess box, ie the line edit widget, if enabled
        """
        if (self.user_input_box.isEnabled()):
            self.user_input_box.setEnabled(False)
