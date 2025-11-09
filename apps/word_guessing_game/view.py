"""Creates the GUI for the word guessing game"""
import os

from PySide6.QtWidgets import QGridLayout, QMainWindow, QWidget
from PySide6.QtCore import Qt


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
