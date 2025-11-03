"""
Class that implements the logic for the translator.
Enables translation from emoji to text with options such as
binary, first letter of emoji, middle letter of emoji, last letter of emoji,
full meaning of emoji
"""
from emot.emo_unicode import UNICODE_EMOJI, UNICODE_EMOJI_ALIAS, EMOTICONS_EMO
from flashtext import KeywordProcessor


class Translator:
    """Implements the translator logic"""

    def __init__(self):
        self.message = ""
        self.binary_result = ""
        self.first_letter_only = ""
        self.middle_letter_only = ""
        self.last_letter_only = ""
        self.full_meaning = ""

        # setting up the emoji dictionary for processing
        # keyword processor will do the replacement
        temp = {**UNICODE_EMOJI, **UNICODE_EMOJI_ALIAS, **EMOTICONS_EMO}
        self.all_emoji_dict = {}
        for key, val in temp.items():
            new_val = val.replace(":", "").replace("_", " ").strip()
            self.all_emoji_dict[key] = new_val
        self.kp_all_emoji = KeywordProcessor()
        for k, v in self.all_emoji_dict.items():
            self.kp_all_emoji.add_keyword(k, v)

    def translate_emoji(self):
        """extracts the emojis from the text and puts the first letter"""
        if self.message:
            result_first_letter = []
            result_middle_letter = []
            result_last_letter = []
            result_full_word = []
            message_list_form = self.message.split(" ")
            mappings = self.kp_all_emoji.get_all_keywords()
            for el in message_list_form:
                if el not in mappings:
                    result_first_letter.append(el)
                    result_middle_letter.append(el)
                    result_last_letter.append(el)
                    result_full_word.append(el)
                else:
                    val = mappings[el]
                    first_letter = val[0]
                    middle_letter = val[(len(val) // 2)]
                    last_letter = val[-1]

                    result_first_letter.append(first_letter)
                    result_middle_letter.append(middle_letter)
                    result_last_letter.append(last_letter)
                    result_full_word.append(val)

            self.first_letter_only = " ".join(result_first_letter)
            self.middle_letter_only = " ".join(result_middle_letter)
            self.last_letter_only = " ".join(result_last_letter)
            self.full_meaning = " ".join(result_full_word)

            binary_str = self.convert_to_binary(result_full_word)
            self.binary_result = binary_str

    def convert_to_binary(self, word_list):
        """
        converts elements in word_list into its binary representation
        """
        result = []
        for w in bytearray(word_list, 'utf-8'):
            new_w = format(w, '08b')
            result.append(new_w)
        return ''.join(result)
