import numpy as np
from PySide6.QtCore import QObject, Qt, QTimer, Slot
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

        # timer for the db level, clip level and meter bar
        self.timer = QTimer()
        self.timer.setInterval(75)
        self.timer.timeout.connect(self.timer_tick)


    def compute_byte_slice_size(self):
        current_sample_rate = self.audio_config.rate
        current_channels = int(self.audio_config.channels)
        current_sample_format = self.audio_config.sample_format
        if current_sample_format == "int16":
            bytes_per_sample = 2
        else:
            bytes_per_sample = 4
        window_ms = 150  # in milliseconds
        frames_in_window = int(current_sample_rate * (window_ms / 1000))
        bytes_per_frames = current_channels * bytes_per_sample
        bytes_in_window = frames_in_window * bytes_per_frames

        current_byte_frame = (self.audio_recorder_logic.
                              get_raw_bytes(self.audio_recorder_logic.frames))
        tail = current_byte_frame[-bytes_in_window:]
        if len(tail) == 0:
            return (0, 0, 0, False)
        rem = len(tail) % bytes_per_frames
        if rem != 0:
            tail = tail[:-rem]

        # normalization
        if current_sample_format == "int16":
            int_array = np.frombuffer(tail, dtype=np.int16)
            normalized_float_array = ((int_array.astype('float32') / 32768.0)
                                      .reshape(-1, current_channels))
        elif current_sample_format == "int32":
            int_array = np.frombuffer(tail, dtype=np.int32)
            normalized_float_array = ((int_array.astype('float32') / 2147483648.0).
                                      reshape(-1, current_channels))
        elif current_sample_format == "float32":
            normalized_float_array = (np.frombuffer(tail).reshape(-1, current_channels))

        samples = np.mean(np.abs(normalized_float_array), axis=1)
        rms = np.sqrt(np.mean(samples ** 2))
        peak = np.max(np.abs(samples))
        db = 20 * np.log10(rms + 1e-12)
        if peak >= 0.999:
            is_clipping = True
        else:
            is_clipping = False
        return (rms, peak, db, is_clipping)

    @Slot(bool)
    def timer_tick(self):
        """
        does the computation for the VU, clip and db
        """


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
