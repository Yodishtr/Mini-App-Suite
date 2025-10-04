"""
It allows the user to simply run this app.

"""
import signal


ONE_ROUND = 1
FIVE_ROUND = 5
TEN_ROUND = 10
FIFTY_ROUND = 50
HUNDRED_ROUND = 100

EASY_DIFFICULTY_STR = "EASY"
MEDIUM_DIFFICULTY_STR = "MEDIUM"
HARD_DIFFICULTY_STR = "HARD"

_RPS_APP = None


def _clear_rps_app():
    global _RPS_APP
    _RPS_APP = None


def run():
    """
    Runs the app
    """
    import sys
    from PySide6.QtWidgets import QApplication
    from apps.rock_paper_scissors.app import RockPaperScissorsApp

    global _RPS_APP
    if not QApplication.instance():
        app = QApplication(sys.argv)
        _RPS_APP = RockPaperScissorsApp()
        _RPS_APP.views.show()
        _RPS_APP.destroyed.connect(_clear_rps_app)
        return app.exec()
    else:
        if _RPS_APP is not None:
            _RPS_APP.views.show()
            _RPS_APP.destroyed.connect(_clear_rps_app)
        else:
            _RPS_APP = RockPaperScissorsApp()
            _RPS_APP.views.show()
            _RPS_APP.destroyed.connect(_clear_rps_app)
        return 0
