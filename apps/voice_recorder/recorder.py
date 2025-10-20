"""
Implements the recorder logic for the voice recorder
"""
import threading
from dataclasses import dataclass
from typing import Optional

import numpy as np
import pyaudio

# Global variables for the formats and numpy array types for decoding
_SAMPLE_FORMAT = {
    "int16": pyaudio.paInt16,
    "int24": pyaudio.paInt24,
    "int32": pyaudio.paInt32,
    "float32": pyaudio.paFloat32
}

_NP_DTYPES = {
    "int16": np.int16,
    "int24": np.int32,
    "int32": np.int32,
    "float32": np.float32
}

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
        devices = []
        number_of_devices = self.audio_system.get_device_count()
        for i in range(number_of_devices):
            current_device_info = self.audio_system.get_device_info_by_index(i)
            if (int(current_device_info.get("maxInputChannels", 0)) > 0):
                devices.append({
                    "index": i,
                    "name": current_device_info.get("name"),
                    "rate": int(current_device_info.get("defaultSampleRate", 0)),
                    "channels": int(current_device_info.get("maxInputChannels", 0))
                })
        return devices

    def start(self):
        """
        Starts the recording of the audio using the PyAudio library. Stores the recorded audio in
        the frames attribute of the AudioRecorder object
        """
        # the recording is running check:
        if self.in_stream is not None:
            return

        current_format = _SAMPLE_FORMAT[self.audio_config.sample_format]
        self.frames.clear()

        def _callback(data_in, frame_count, time_info, status_flag):
            if self.running.is_set():
                with self.lock:
                    self.frames.append(data_in)
                return (None, pyaudio.paContinue)
            else:
                return (None, pyaudio.paComplete)

        self.in_stream = self.audio_system.open(format=current_format,
                                                channels=self.audio_config.channels,
                                                rate=self.audio_config.rate,
                                                input=True,
                                                input_device_index=self.audio_config.device_index,
                                                frames_per_buffer=self.audio_config.chunk,
                                                stream_callback=_callback)
        self.running.set()
        self.in_stream.start_stream()

    def is_recording(self):
        """
        Checks the thread where the recording is currently being done.
        Returns True if a recording is currently being made and False otherwise.
        """
        return self.running.is_set()

    def stop(self):
        """
        Stops the recording and releases the thread event for when recording is running
         that signifies pyAudio background thread is working
        """
        if (not self.is_recording()) or (self.in_stream is None):
            return
        else:
            self.running.clear()
            self.in_stream.stop_stream()
            self.in_stream.close()
            self.in_stream = None

    def get_raw_bytes(self):
        """
        Concatenate the byte chunks in the self.frame into a single byte.
        """
        with self.lock:
            concatenated_chunks = b"".join(self.frames)
            return concatenated_chunks

    def get_numpy(self):
        """
        Convert raw bytes to a float32 array in [-1, 1], because most edits are simpler
        in a normalized float domain.
        format == "int24" not supported
        should be called after stop
        """
        raw_data = self.get_raw_bytes()
        if not raw_data:
            return np.empty((0, self.audio_config.channels), dtype=np.float32)
        current_format = self.audio_config.sample_format
        if current_format == "int16":
            numpy_arr = (np.frombuffer(raw_data, _NP_DTYPES[current_format])
                         .astype(np.float32) / 32768.0)
        elif current_format == "int32":
            numpy_arr = (np.frombuffer(raw_data, _NP_DTYPES[current_format])
                         .astype(np.float32) / 2147483648.0)
        elif current_format == 'float32':
            numpy_arr = np.frombuffer(raw_data, _NP_DTYPES[current_format])
        else:
            raise ValueError("Unsupported Format")

        if self.audio_config.channels > 1:
            remainder_sample = len(raw_data) % self.audio_config.channels
            if remainder_sample == 0:
                numpy_arr = numpy_arr.reshape(-1, self.audio_config.channels)
            else:
                
        else:
            numpy_arr = numpy_arr.reshape(-1, 1)
        return numpy_arr
