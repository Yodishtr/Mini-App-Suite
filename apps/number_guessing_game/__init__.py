"""
Allows the user to simply run the app
"""

_NGG_APP = None


def _clear_NGG_APP():
    global _NGG_APP
    _NGG_APP = None


def run():
    """
    Runs the app for the number guessing game
    """
    import sys
    from PySide6.QtWidgets import QApplication
    from apps.number_guessing_game.app import NumberGuessingApp

    global _NGG_APP
    if not QApplication.instance():
        app = QApplication(sys.argv)
        _NGG_APP = NumberGuessingApp()
        if not app.quitOnLastWindowClosed():
            app.setQuitOnLastWindowClosed(True)
        _NGG_APP.views.show()
        _NGG_APP.destroyed.connect(_clear_NGG_APP)
        return app.exec()
    else:
        if _NGG_APP:
            _NGG_APP.views.show()
            _NGG_APP.destroyed.connect(_clear_NGG_APP)
        else:
            _NGG_APP = NumberGuessingApp()
            _NGG_APP.views.show()
            _NGG_APP.destroyed.connect(_clear_NGG_APP)
            return 1
