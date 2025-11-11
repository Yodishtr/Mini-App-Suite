"""Creates the GUI for the word guessing game"""
import os

from PySide6.QtWidgets import QGridLayout, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QPushButton, \
    QVBoxLayout, QWidget
from PySide6.QtCore import Qt


class LetterTile(QLabel):
    """A Qlabel that acts as a tile to display the users guess"""
    def __init__(self, size=48, parent=None):
        super().__init__(parent)
        self.setFixedSize(size, size)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("""
            QLabel{
                border: 2px solid #dcdcdc; 
                border-radius: 6px;
                font-weight: 600; 
                font-size: 20px; 
                background: #ffffff; 
            }
            QLabel[status="filled"]  { border-color: #b8b8b8; }
            QLabel[status="correct"] { 
                background: #6aaa64; 
                color: white; 
                border-color: #6aaa64; 
            }
            QLabel[status="present"] { 
                background: #c9b458; 
                color: white; 
                border-color: #c9b458; 
            }
            QLabel[status="absent"]  { 
                background: #787c7e; 
                color: white; 
            }
        """)
        self.clear_tile()

    def clear_tile(self):
        """Clears the tiles to be ready to accept the user's guess"""
        self.setText("")
        self.setProperty("status", "")
        self._refresh()

    def set_char(self, ch):
        """sets the input char for the tile"""
        if ch:
            self.setText(ch.lower())
            self.setProperty("status", "filled")
        else:
            self.setText("")
            self.setProperty("status", "")
        self._refresh()

    def set_state(self, state):
        """Sets the state of the tile based on the user input (correct, present, absent)"""
        self.setProperty("status", state)
        self._refresh()

    def _refresh(self):
        """Removes the styles applied to the ui"""
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()


class OneBoardRow(QWidget):
    """A single row board to display the letter tiles representing the user's input"""

    def __init__(self, parent=None):
        """constructor to build the row displaying the player's input"""
        super().__init__(parent)
        self.tiles = []
        self.word_length = 0
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(5)

    def setup_tiles(self, word_len):
        """clears the letter tiles and makes them ready to accept new input"""
        for t in self.tiles:
            t.setParent(None)
        self.tiles.clear()
        self.word_length = word_len
        for i in range(word_len):
            tile = LetterTile(self)
            self.tiles.append(tile)
            self.layout.addWidget(tile)

    def set_text(self, txt):
        """sets the letters input by the user into the letter tiles"""
        if not txt:
            text = ""
        else:
            text = txt[:self.word_length]
        for i in range(self.word_length):
            if i < len(text):
                self.tiles[i].set_char(text[i])
            else:
                self.tiles[i].set_char("")

    def reveal_state(self, states):
        """changes the states of each letter tile according to the game logic feedback"""
        for i, st in enumerate(states[:self.word_length]):
            self.tiles[i].set_state(st)

    def clear_all(self):
        """clears all the tiles in the row to change the tiles"""
        for t in self.tiles:
            t.clear_tile()


class WordGuesserView(QMainWindow):
    """Class implementing the GUI for the game"""

    def __init__(self):
        super().__init__()
        BASE_PATH = os.path.dirname(__file__)

        # central widget
        central_widget = QWidget()
        central_widget.setObjectName("central")
        self.setCentralWidget(central_widget)
        central_widget_layout = QGridLayout()
        central_widget.setLayout(central_widget_layout)
        central_widget.setAttribute(Qt.WA_StyledBackground, True)

        background_image = os.path.join(BASE_PATH, "wg_bckg.jpeg")
        central_widget.setStyleSheet(f"""
        QWidget#central{{
            background-image: url("{background_image}");
        }}
        """)

        # menu box
        menu_layout = QHBoxLayout()

        # difficulty element of the menu
        difficulty_layout = QVBoxLayout()
        difficulty_title = QLabel("Difficulty")
        self.difficulty_chosen = QLabel("")
        difficulty_layout.addWidget(difficulty_title)
        difficulty_layout.addSpacing(5)
        difficulty_layout.addWidget(self.difficulty_chosen)
        menu_layout.addLayout(difficulty_layout)
        menu_layout.addSpacing(5)

        # guess count
        guesses_layout = QVBoxLayout()
        guess_count_title = QLabel("Guess Count:")
        self.guess_count = QLabel("")
        guesses_layout.addWidget(guess_count_title)
        guesses_layout.addSpacing(5)
        guesses_layout.addWidget(self.guess_count)
        menu_layout.addLayout(guesses_layout)
        menu_layout.addSpacing(5)

        # choose difficulty buttons
        choose_diff_layout = QHBoxLayout()
        self.easy_difficulty_button = QPushButton("Easy")
        self.medium_difficulty_button = QPushButton("Medium")
        self.hard_difficulty_button = QPushButton("Hard")
        choose_diff_layout.addWidget(self.easy_difficulty_button)
        choose_diff_layout.addSpacing(5)
        choose_diff_layout.addWidget(self.medium_difficulty_button)
        choose_diff_layout.addSpacing(5)
        choose_diff_layout.addWidget(self.hard_difficulty_button)

        # layout for the user to input their guesses and display it
        user_input_layout = QHBoxLayout()
        self.user_input = QLineEdit()
        self.user_input.setMaxLength(15)
        self.user_input.setPlaceholderText("Write your guess!")
        self.submit_button = QPushButton("Submit")
        user_input_layout.addWidget(self.user_input)
        user_input_layout.addSpacing(10)
        user_input_layout.addWidget(self.submit_button)

        board_layout = QVBoxLayout()
        self.board = OneBoardRow(self)
        board_layout.addWidget(self.board)
        board_layout.addSpacing(10)
        board_layout.addLayout(user_input_layout)

        # central layout setup for the ui
        central_widget_layout.addLayout(menu_layout, 0, 1, 2, 6)
        central_widget_layout.addLayout(choose_diff_layout, 3, 1, 1, 6)
        central_widget_layout.addLayout(board_layout, 5, 1, 5, 6)
