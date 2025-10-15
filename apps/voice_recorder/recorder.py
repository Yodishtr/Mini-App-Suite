"""
Implements the recorder logic for the voice recorder
"""
import threading
from dataclasses import dataclass
from typing import Optional

import pyaudio


@dataclass
class AudioConfig:
    """Holds the parameters necessary for the audio file to be processed"""
    rate: int = 44100
    channels: int = 1
    chunk: int = 1024
    sample_format: str = "int16"
    device_index: Optional[int] = None
    output_dir: str = "recordings"
    default_filename_prefix: str = "take"
    auto_increment: bool = True


class AudioRecorder:
    """
    A non-blocking microphone recorder using PyAudio.
    - start(): opens the audio stream and buffers the audio into bytes based on chunk size
    - stop(): stops & closes the recording stream
    - save_wav(path): writes the current recorded buffer to a .Wav file that can be played
    - get_numpy(): returns a mono/stereo numpy array (shape, [n, ch])
    """
    def __init__(self, audio_config):
        """Initializes the audio recorder object with the required settings and utilities"""
        # keeps my recording settings (rate, channels, chunk size, etc.)
        self.audio_config = audio_config

        # opens a handle to the audio subsystem.
        # it creates its own thread so you use the threading.Event() to communicate
        # between the main thread which will be any method in this current object
        # and the pyaudio thread
        self.audio_system = pyaudio.PyAudio()

        # placeholder for the microphone stream
        self.in_stream = None

        # placeholder for the speaker stream to play the recording.
        # its gonna be closed in pause/stop playing
        self.out_stream = None

        # list to hold all the audio chunks to be recorded
        self.frames = []

        # ensures safe access to _frames (since callbacks run in another thread) can also be used
        # when playing the audio recording
        self.lock = threading.Lock()

        # flag that tells the callback whether to keep recording
        self.running = threading.Event()

        # play_pos will read next from the recorded bytes.
        # play() uses it, pause() preserves it, stop_playback() resets it to 0.
        self.play_pos = 0

        # indicate active playback
        self.is_playing = False

        # enables us to check if the recording is currently being played
        self.playing = threading.Event()

    def list_devices_connected(self):
        """
        returns a dictionary of the devices connected with the key = device name and values are the
        maximum input channels, maximum output channels and the default sampling rate of the
        device.
        """
        devices = {}
        number_of_devices = self.audio_system.get_device_count()
        for i in range(number_of_devices):
            current_device = self.audio_system.get_device_info_by_index(i)
            current_device_name = current_device["name"]
            current_device_input_channels = current_device["maxInputChannels"]
            current_device_output_channels = current_device["maxOutputChannels"]
            current_device_default_sample_rate = current_device["defaultSampleRate"]
            devices[current_device_name] = [current_device_input_channels,
                                            current_device_output_channels,
                                            current_device_default_sample_rate]
