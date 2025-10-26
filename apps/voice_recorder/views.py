"""
Creates the specific UI for the voice recorder app.
"""
import os.path

from PySide6.QtWidgets import QGridLayout, QHBoxLayout, QMainWindow, QPushButton, QWidget
from PySide6.QtGui import QAction


class VoiceRecorderView(QMainWindow):
    """A class that represents the main window display for the voice recorder"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Welcome to the Voice Recorder App")
        self.setGeometry(400, 400, 800, 600)
        self.exit = QAction("Exit the application", self)
        self.exit.triggered.connect(self._exit_app)
        self.addAction(self.exit)

        central_widget = QWidget()
        central_widget.setObjectName("central")
        self.setCentralWidget(central_widget)
        central_layout = QGridLayout(central_widget)
        BASE_PATH = os.path.dirname(__file__)
        background_image = os.path.join(BASE_PATH, "VR_background.webp")
        central_widget.setStyleSheet(f"""
        QWidget#central{{
            background-image: url("{background_image}");
            
        }}
        """)

        menu_options_layout = QHBoxLayout()
        self.record_button = QPushButton("Record")





    def _exit_app(self):
        """Closes the app"""
        self.close()
