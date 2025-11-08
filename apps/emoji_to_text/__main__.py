"""Allows users to run the app without scripts"""
import sys
from apps import emoji_to_text


def main():
    """Starts the QtApplication for the emoji to text app"""
    status = emoji_to_text.run()
    sys.exit(status)


if __name__ == "__main__":
    main()
