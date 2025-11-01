"""
Allows the user to simply run the app from the terminal
"""

_VR_APP = None


def clear_VR_APP():
    global _VR_APP
    _VR_APP = None


def run():
    """
    Runs the app for the voice recorder
    """
    import sys
    from PySide6.QtWidgets import QApplication
    from apps.voice_recorder.app import VoiceRecorder

    global _VR_APP
    if not QApplication.instance():
        app = QApplication(sys.argv)
        _VR_APP = VoiceRecorder()
        if not app.quitOnLastWindowClosed():
            app.setQuitOnLastWindowClosed(True)

        _VR_APP.audio_recorder_views.show()
        _VR_APP.destroyed.connect(clear_VR_APP)
        return app.exec()
    else:
        if _VR_APP:
            _VR_APP.audio_recorder_views.show()
            _VR_APP.destroyed.connect(clear_VR_APP)
        else:
            _VR_APP = VoiceRecorder()
            _VR_APP.audio_recorder_views.show()
            _VR_APP.destroyed.connect(clear_VR_APP)
            return 1
