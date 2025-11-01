"""
Allows users to run the app without additional scripts
"""
import sys
from apps import voice_recorder

def main():
    """
    Starts and runs the QT application for the voice recorder
    """
    status = voice_recorder.run()
    sys.exit(status)

if __name__ == "__main__":
    main()
