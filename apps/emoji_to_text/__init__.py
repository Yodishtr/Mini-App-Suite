"""Allows the user to import the app as a package"""

_ETT_APP = None


def clear_emoji_app():
    global _ETT_APP
    _ETT_APP = None


def run():
    """
    Runs the app for the emoji to text game
    """
    import sys
    from PySide6.QtWidgets import QApplication
    from apps.emoji_to_text.controller import EmojiToTextController

    global _ETT_APP
    if not QApplication.instance():
        app = QApplication(sys.argv)
        _ETT_APP = EmojiToTextController()
        if not app.quitOnLastWindowClosed():
            app.setQuitOnLastWindowClosed()
        _ETT_APP.views.show()
        _ETT_APP.destroyed.connect(clear_emoji_app)
        return app.exec()
    else:
        if _ETT_APP:
            _ETT_APP.views.show()
            _ETT_APP.destroyed.connect(clear_emoji_app)
        else:
            _ETT_APP = EmojiToTextController()
            _ETT_APP.views.show()
            _ETT_APP.destroyed.connect(clear_emoji_app)
            return 1
