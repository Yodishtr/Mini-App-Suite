"""A file reader class that loads the files containing the words for the guesses"""


class WordProvider:
    """Class that contains the file reading and saving function"""

    def __init__(self, easy_path, medium_path, hard_path):
        self.easy_diff_path = easy_path
        self.medium_diff_path = medium_path
        self.hard_diff_path = hard_path
        self.easy_lst = []
        self.easy_count = 0
        self.medium_lst = []
        self.medium_count = 0
        self.hard_lst = []
        self.hard_count = 0

    def load_easy_words(self):
        """Loads and stores the words from the .txt file containing easy words"""
        try:
            with open(self.easy_diff_path, "r") as ef:
                curr_word = ef.readline()
                while curr_word:
                    self.easy_lst.append(curr_word.strip())
                    self.easy_count += 1
                    curr_word = ef.readline()

        except FileNotFoundError:
            print("Error: file containing easy words not found")
        except Exception as e:
            print(f"An error occurred: {e}")

    def load_medium_words(self):
        """Loads and stores the words from the .txt file containing medium words"""
        try:
            with open(self.medium_diff_path, "r") as mf:
                curr_word = mf.readline()
                while curr_word:
                    self.medium_lst.append(curr_word.strip())
                    self.medium_count += 1
                    curr_word = mf.readline()

        except FileNotFoundError:
            print("Error: file containing medium words not found")
        except Exception as e:
            print(f"An error occurred: {e}")

    def load_hard_words(self):
        """Loads and stores the words from the .txt file containing hard words"""
        try:
            with open(self.hard_diff_path, "r") as hf:
                curr_word = hf.readline()
                while curr_word:
                    self.hard_lst.append(curr_word.strip())
                    self.hard_count += 1
                    curr_word = hf.readline()

        except FileNotFoundError:
            print("Error: file containing hard words not found")
        except Exception as e:
            print(f"An error occurred: {e}")
