"""
Creates the specific UI for the voice recorder app.
"""
import os.path

from PySide6.QtWidgets import QGridLayout, QHBoxLayout, QLabel, QMainWindow, QMessageBox, \
    QProgressBar, \
    QPushButton, QVBoxLayout, QWidget
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt


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
        QLabel#ClipLevel{{
            background-color: grey;
            border-radius: 6px;
        }}
        """)

        # main options button
        menu_options_layout = QHBoxLayout()
        self.record_button = QPushButton("Record")
        self.pause_button = QPushButton("Pause")
        self.stop_button = QPushButton("Stop")
        self.play_button = QPushButton("Play")
        self.save_wav_button = QPushButton("Save Wav File")
        menu_options_layout.addWidget(self.record_button)
        menu_options_layout.addWidget(self.pause_button)
        menu_options_layout.addWidget(self.stop_button)
        menu_options_layout.addWidget(self.play_button)
        menu_options_layout.addWidget(self.save_wav_button)

        # recording in progress (red when active and grey when incactive),
        # recording paused (black when paused and grey when not),
        # no recording and playing (recording normal and paused label normal)
        # and not playing indicators. will just modify the colors
        indicators_layout = QHBoxLayout()
        self.recording_label = QLabel("Recording")
        self.recording_paused_label = QLabel("Paused")
        self.playing_label = QLabel("Playing")
        indicators_layout.addWidget(self.recording_label)
        indicators_layout.addSpacing(5)
        indicators_layout.addWidget(self.recording_paused_label)
        indicators_layout.addSpacing(5)
        indicators_layout.addWidget(self.playing_label)

        # level bar to show the recording sound level
        progress_bar_layout = QHBoxLayout()
        self.level_bar = QProgressBar()
        self.level_bar.setTextVisible(False)
        self.level_bar.setFixedHeight(10)
        self.level_bar.setOrientation(Qt.Horizontal)
        self.level_bar.setMinimum(0)
        self.level_bar.setMaximum(100)
        progress_bar_layout.addWidget(self.level_bar, 2)
        progress_bar_layout.addSpacing(10)
        # decibel level label
        decibel_level_layout = QVBoxLayout()
        decibel_level_title = QLabel("dB level")
        self.decibel_level = QLabel("")
        decibel_level_layout.addWidget(decibel_level_title)
        decibel_level_layout.addWidget(self.decibel_level)
        progress_bar_layout.addLayout(decibel_level_layout, 0)


        # clip level to indicate if the sound of recording is too loud
        clip_level_layout = QHBoxLayout()
        self.clip_level = QLabel()
        self.clip_level.setFixedSize(12, 12)
        self.clip_level.setObjectName("ClipLevel")
        clip_level_layout.addWidget(self.clip_level)

        # shows a popup box for when there are important messages
        message_box_layout = QVBoxLayout()
        message_title = QLabel("Oye Oye Un Message pour vous messire")
        self.message_box = QMessageBox()
        self.message_box.setIcon(QMessageBox.Icon.Information)
        self.message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        message_box_layout.addWidget(message_title)
        message_box_layout.addSpacing(5)
        message_box_layout.addWidget(self.message_box)

        # adding the different layouts to the central layout
        central_layout.addLayout(menu_options_layout, 0, 0, 2, 6)
        central_layout.addLayout(indicators_layout, 3, 0, 2, 4)
        central_layout.addLayout(progress_bar_layout, 4, 0, 2, 6)
        central_layout.addLayout(clip_level_layout, 6, 0, 1, 1)
        central_layout.addLayout(message_box_layout, 8, 0, 2, 4)

    def _exit_app(self):
        """Closes the app"""
        self.close()

    def setVULevel(self, level):
        """
        updates the progress bar
        """
        current_level = level
        if current_level < 0:
            current_level = 0
        elif current_level > 1:
            current_level = 1
        progress_bar_value = round(current_level * 100)
        self.level_bar.setValue(progress_bar_value)

    def setPeakClipping(self, is_clipping):
        """
        changes the color of the clip light's label
        """
        if is_clipping:
            self.clip_level.setStyleSheet("background-color: red; border-radius: 6px;")
        else:
            self.clip_level.setStyleSheet("background-color: grey; border-radius: 6px;")

    def setDBLabel(self, text):
        """
        updates the dB level of the label to correspond to the sound level
        """
        self.decibel_level.setText(text)
