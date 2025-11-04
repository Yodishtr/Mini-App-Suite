"""
Controller for the emoji to text app.
"""
from PySide6.QtCore import QObject, Slot
from apps.emoji_to_text.view import EmojiToTextView
from apps.emoji_to_text.translator import Translator

class EmojiToTextController(QObject):
    """Acts as a mediator between the GUI and the logic behind the app"""

    def __init__(self):
        super().__init__()
        self.views = EmojiToTextView()
        self.translator_logic = Translator()

        self.views.translate_button.clicked.connect(self.do_translation)


    @Slot(bool)
    def do_translation(self):
        self.translator_logic.message = self.views.input_message.text()
        self.translator_logic.translate_emoji()
