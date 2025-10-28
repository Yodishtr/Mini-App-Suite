from PySide6.QtCore import QObject, Qt, Slot
from apps.voice_recorder.recorder import (AudioRecorder, AudioConfig,
                                          NoRecordingAvailable, PlayRecordingInSession,
                                          RecordingInSession)
from enum import Enum, auto

from apps.voice_recorder.views import VoiceRecorderView


class State(Enum):
    """State machine representing the different states of the Voice Recorder"""
    IDLE = auto()
    RECORDING = auto()
    STOPPED = auto()
    PLAYING = auto()
    PAUSED = auto()


class VoiceRecorder(QObject):
    """
    Represents the entry point for the GUI to display the voice recorder and integrates
    the logic for the gui recorded
    """

    def __init__(self):
        super().__init__()
        self.audio_config = AudioConfig()
        self.audio_recorder_logic = AudioRecorder(self.audio_config)
        self.audio_recorder_views = VoiceRecorderView()
        self.state_machine = State.IDLE

        # connect buttons to handlers.
        self.audio_recorder_views.record_button.clicked.connect(self.record_requested)
        self.audio_recorder_views.pause_button.clicked.connect(self.pause_requested)
        self.audio_recorder_views.stop_button.clicked.connect(self.stop_requested)
        self.audio_recorder_views.play_button.clicked.connect(self.play_requested)
        self.audio_recorder_views.save_wav_button.clicked.connect(self.save_wav_requested)

    @Slot(bool)
    def record_requested(self):
        """
        Calls the method from the audio recorder class to start the recording
        """
        try:
            self.state_machine = State.RECORDING
            self.audio_recorder_views.recording_label.setStyleSheet("background-color: red;")
            self.audio_recorder_logic.start()
        except (RecordingInSession):
            self.audio_recorder_views.message_box.setText("Recording in Session")

    @Slot(bool)
    def pause_requested(self):
        """
        calls the method from the audio recorder to pause the playback and the recording.
        """
        if self.state_machine == State.PLAYING:
            self.audio_recorder_logic.pause_playing()
            self.state_machine = State.PAUSED
        else:
            self.audio_recorder_views.message_box.setText("Pause button is only for playback")

    @Slot(bool)
    def stop_requested(self):
        """
        calls the method from the audio recorder to stop the playback and the recording.
        """
        if self.state_machine == State.RECORDING:
            self.audio_recorder_logic.stop()
            self.state_machine = State.STOPPED
            self.audio_recorder_views.recording_label.setStyleSheet("background-color: grey;")

        elif self.state_machine == State.PLAYING:
            self.audio_recorder_logic.stop_playing()
            self.state_machine = State.STOPPED
        else:
            self.audio_recorder_views.message_box.setText("Use your brain bruh! "
                                                          "nothing else to stop")

    @Slot(bool)
    def play_requested(self):
        """
        calls the method from the audio recorder to play the recently recorded audio.
        """
        try:
            self.audio_recorder_logic.play_audio()
            self.state_machine = State.PLAYING
        except (NoRecordingAvailable):
            self.audio_recorder_views.message_box.setText("No Recording to play. Record Something")

        except (PlayRecordingInSession):
            self.audio_recorder_views.message_box.setText("Recording currently being played.")

    @Slot(bool)
    def save_wav_requested(self):
        """
        calls the method from the audio recorder to save the currently recorded audio to a
        wav file in the recordings directory from the audio config.
        """
        try:
            self.audio_recorder_logic.save_wav()
            self.state_machine = State.IDLE
        except (RecordingInSession):
            self.audio_recorder_views.message_box.setText("Recording rn! Cant save")
