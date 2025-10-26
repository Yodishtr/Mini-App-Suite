from PySide6.QtCore import QObject, Qt, Slot
from apps.voice_recorder.recorder import (AudioRecorder, AudioConfig,
                                          NoRecordingAvailable, PlayRecordingInSession,
                                          RecordingInSession)
from enum import Enum, auto


class RecordingState(Enum):
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
