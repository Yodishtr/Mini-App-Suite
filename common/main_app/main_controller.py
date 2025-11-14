"""Class representing the controller for the main app"""
from PySide6.QtCore import QObject, Slot
from common.main_app.main_logic import MainAppLogic
from common.main_app.main_view import MainAppView


class MainAppController(QObject):
    """ handles the display of the apps etc"""

    def __init__(self):
        super().__init__()
        self.main_app_logic = MainAppLogic()
        self.main_app_views = MainAppView()

        self.main_app_views.emoji_app_btn.clicked.connect(self.start_emoji)
        self.main_app_views.number_guess_btn.clicked.connect(self.start_number_guesser)
        self.main_app_views.rock_paper_scissors_btn.clicked.connect(self.start_rps)
        self.main_app_views.voice_recorder_btn.clicked.connect(self.start_vr)
        self.main_app_views.word_guess_btn.clicked.connect(self.start_wg)

    @Slot(bool)
    def start_emoji(self):
        """Launches the emoji to text app when the user clicks on that button"""
        self.main_app_logic.launch_emoji_app()

    @Slot(bool)
    def start_number_guesser(self):
        """Launches the number guesser app when the user clicks on that button"""
        self.main_app_logic.launch_number_guessing_app()

    @Slot(bool)
    def start_rps(self):
        """Launches the rock paper scissors app when the user clicks on that button"""
        self.main_app_logic.launch_rock_paper_scissors_app()

    @Slot(bool)
    def start_vr(self):
        """Launches the voice recording app when the user clicks on that button"""
        self.main_app_logic.launch_voice_recorder_app()

    @Slot(bool)
    def start_wg(self):
        """Launches the word guesser app when the user clicks on that button"""
        self.main_app_logic.launch_word_guesser_app()
