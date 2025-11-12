"""Allows the user to run the app"""

_WGG_APP = None


def _clear_WGG_APP():
    global _WGG_APP
    _WGG_APP = None


def run():
    """
    Runs the app for the word guessing game
    """
    import sys
    from PySide6.QtWidgets import QApplication
    from apps.word_guessing_game.controller import WordGuesserController

    global _WGG_APP
    if not QApplication.instance():
        app = QApplication(sys.argv)
        _WGG_APP = WordGuesserController()
        if not app.quitOnLastWindowClosed():
            app.setQuitOnLastWindowClosed(True)
        _WGG_APP.views.show()
        _WGG_APP.destroyed.connect(_clear_WGG_APP)
        return app.exec()
    else:
        if _WGG_APP:
            _WGG_APP.views.show()
            _WGG_APP.destroyed.connect(_clear_WGG_APP)
        else:
            _WGG_APP = WordGuesserController()
            _WGG_APP.views.show()
            _WGG_APP.destroyed.connect(_clear_WGG_APP)
            return 1
