"""
Allows users to run the app without additional scripts
"""
import sys

from apps import rock_paper_scissors


def main():
    """
    starts the QtApplication

    """
    status = rock_paper_scissors.run()
    sys.exit(status)


if __name__ == "__main__":
    main()
