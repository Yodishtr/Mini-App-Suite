"""A class representing the view of the main app"""
import os

from PySide6.QtWidgets import QGridLayout, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QPushButton, \
    QVBoxLayout, QWidget
from PySide6.QtCore import Qt


class MainAppView(QMainWindow):
    """A main window app that enables the user to simply start any game"""

    def __init__(self):
        super().__init__()
        BASE_PATH = os.path.dirname(__file__)

        central_widget = QWidget()
        central_widget.setObjectName("central")
        self.setCentralWidget(central_widget)
        central_widget_layout = QGridLayout()
        central_widget.setLayout(central_widget_layout)
        central_widget.setAttribute(Qt.WA_StyledBackground, True)
        background_image = os.path.join(BASE_PATH, "faith-spark-background1.jpg")
        central_widget.setStyleSheet(f"""
        QWidget#central{{
            background-image: url("{background_image}");
        }}
        """)

        # button options
        button_app_layout = QVBoxLayout()
        self.emoji_app_btn = QPushButton("Emoji To Text")
        self.number_guess_btn = QPushButton("Number Guessing Game")
        self.rock_paper_scissors_btn = QPushButton("Rock Paper Scissors")
        self.voice_recorder_btn = QPushButton("Voice Recorder")
        self.word_guess_btn = QPushButton("Word Guessing Game")
