"""
Allows users to run the app without additional scripts
"""
import sys
from apps import number_guessing_game


def main():
    """
    Starts the QtApplication for the number guessing game
    """
    status = number_guessing_game.run()
    sys.exit(status)


if __name__ == "__main__":
    main()
