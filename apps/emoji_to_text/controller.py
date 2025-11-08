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
        """
        Processes the translation of the text input and fills the required fields
        accordingly.
        """
        self.views.translate_button.setEnabled(False)
        self.translator_logic.message = self.views.input_message.text()
        self.translator_logic.translate_emoji()
        self.views.first_letter_textbox.setText(self.translator_logic.first_letter_only)
        self.views.middle_letter_textbox.setText(self.translator_logic.middle_letter_only)
        self.views.last_letter_textbox.setText(self.translator_logic.last_letter_only)
        self.views.binary_textbox.setText(self.translator_logic.binary_result)
        self.views.full_meaning_textbox.setText(self.translator_logic.full_meaning)
        self.views.translate_button.setEnabled(True)
