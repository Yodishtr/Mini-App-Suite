"""
Creates the specific UI for rock paper scissors.
Utilizes the common/ui/__init__ as a wrapper to keep fonts, colors and styles
consistent across the app.

"""
from PySide6 import *
from PySide6.QtWidgets import QMainWindow


class MainWindow(QMainWindow):
    """A class that represents the main game window"""
