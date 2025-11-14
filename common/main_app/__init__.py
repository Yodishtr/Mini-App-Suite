"""Allows the user to import the main app as a package to then run it"""

_MAIN_APP = None


def _clear_main_app():
    global _MAIN_APP
    _MAIN_APP = None


def run():
    """Runs the main app"""
    import sys
    from PySide6.QtWidgets import QApplication
    from common.main_app.main_controller import MainAppController

    global _MAIN_APP
    if not QApplication.instance():
        curr_main = QApplication(sys.argv)
        _MAIN_APP = MainAppController()
        if not curr_main.quitOnLastWindowClosed():
            curr_main.setQuitOnLastWindowClosed(True)
        _MAIN_APP.main_app_views.show()
        _MAIN_APP.destroyed.connect(_clear_main_app)
        return curr_main.exec()
    else:
        if _MAIN_APP:
            _MAIN_APP.main_app_views.show()
            _MAIN_APP.destroyed.connect(_clear_main_app)
        else:
            _MAIN_APP = MainAppController()
            _MAIN_APP.main_app_views.show()
            _MAIN_APP.destroyed.connect(_clear_main_app)
            return 1
