"""Handles the logic for managing the different apps in the main app"""
from apps import (emoji_to_text, number_guessing_game, rock_paper_scissors, voice_recorder,
                  word_guessing_game)

class MainAppLogic():
    """A class that represents handling of the logic for enabling the users to use all the apps"""

    def __init__(self):
        self.emoji_to_text_app = emoji_to_text.run
        self.number_guessing_game_app = number_guessing_game.run
        self.rock_paper_scissors_app = rock_paper_scissors.run
        self.voice_recorder_app = voice_recorder.run
        self.word_guessing_game_app = word_guessing_game.run

    def launch_emoji_app(self):
        """Launched the emoji to text app"""
        self.emoji_to_text_app()

    def launch_number_guessing_app(self):
        """Launches the number guessing game app"""
        self.number_guessing_game_app()

    def launch_rock_paper_scissors_app(self):
        """Launches the rock paper scissors game app"""
        self.rock_paper_scissors_app()

    def launch_voice_recorder_app(self):
        """Launches the voice recorder app"""
        self.voice_recorder_app()

    def launch_word_guesser_app(self):
        """Launches the word guesser app"""
        self.word_guessing_game_app()
