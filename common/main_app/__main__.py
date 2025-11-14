"""Runs the main app"""
import sys
from common import main_app


def main():
    """function that runs the app"""
    status = main_app.run()
    sys.exit(status)


if __name__ == "__main__":
    main()
