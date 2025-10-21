"""
Implements the recorder logic for the voice recorder
"""
import os.path
import re
import threading
import wave
from dataclasses import dataclass
from typing import Optional

import numpy as np
import pyaudio

# Global variables for the formats and numpy array types for decoding
_SAMPLE_FORMAT = {
    "int16": pyaudio.paInt16,
    "int32": pyaudio.paInt32,
    "float32": pyaudio.paFloat32
}

_NP_DTYPES = {
    "int16": np.int16,
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

    def get_raw_bytes(self, frames):
        """
        Concatenate the byte chunks in the frames into a single byte.
        """
        with self.lock:
            concatenated_chunks = b"".join(frames)
            return concatenated_chunks

    def get_numpy(self):
        """
        Convert raw bytes to a float32 array in [-1, 1], because most edits are simpler
        in a normalized float domain.
        format == "int24" not supported
        should be called after stop
        """
        raw_data = self.get_raw_bytes(self.frames)
        if not raw_data:
            return np.empty((0, self.audio_config.channels), dtype=np.float32)
        current_format = self.audio_config.sample_format
        if current_format == "int16":
            if self.audio_config.channels > 1:
                frame_bytes = self.audio_config.channels * 2
                remainder_sample = len(raw_data) % frame_bytes
                if remainder_sample == 0:
                    numpy_arr = (np.frombuffer(raw_data, _NP_DTYPES[current_format])
                                 .astype(np.float32) / 32768.0)
                    numpy_arr_result = numpy_arr.reshape(-1, self.audio_config.channels)
                    return numpy_arr_result
                else:
                    new_raw_data = raw_data[:-remainder_sample]
                    numpy_arr = (np.frombuffer(new_raw_data, _NP_DTYPES[current_format])
                                 .astype(np.float32) / 32768.0)
                    numpy_arr_result = numpy_arr.reshape(-1, self.audio_config.channels)
                    return numpy_arr_result
            else:
                numpy_arr = (np.frombuffer(raw_data, _NP_DTYPES[current_format])
                             .astype(np.float32) / 32768.0)
                numpy_arr_result = numpy_arr.reshape(-1, 1)
                return numpy_arr_result

        elif current_format == "int32":
            if self.audio_config.channels > 1:
                frame_bytes = self.audio_config.channels * 4
                remainder_sample = len(raw_data) % frame_bytes
                if remainder_sample == 0:
                    numpy_arr = (np.frombuffer(raw_data, _NP_DTYPES[current_format])
                                 .astype(np.float32) / 2147483648.0)
                    numpy_arr_result = numpy_arr.reshape(-1, self.audio_config.channels)
                    return numpy_arr_result
                else:
                    new_raw_data = raw_data[:-remainder_sample]
                    numpy_arr = (np.frombuffer(new_raw_data, _NP_DTYPES[current_format])
                                 .astype(np.float32) / 2147483648.0)
                    numpy_arr_result = numpy_arr.reshape(-1, self.audio_config.channels)
                    return numpy_arr_result
            else:
                numpy_arr = (np.frombuffer(raw_data, _NP_DTYPES[current_format])
                             .astype(np.float32) / 2147483648.0)
                numpy_arr_result = numpy_arr.reshape(-1, 1)
                return numpy_arr_result

        elif current_format == 'float32':
            if self.audio_config.channels > 1:
                frame_bytes = self.audio_config.channels * 4
                remainder_sample = len(raw_data) % frame_bytes
                if remainder_sample == 0:
                    numpy_arr = np.frombuffer(raw_data, _NP_DTYPES[current_format])
                    numpy_arr_result = numpy_arr.reshape(-1, self.audio_config.channels)
                    return numpy_arr_result
                else:
                    new_raw_data = raw_data[:-remainder_sample]
                    numpy_arr = np.frombuffer(new_raw_data, _NP_DTYPES[current_format])
                    numpy_arr_result = numpy_arr.reshape(-1, self.audio_config.channels)
                    return numpy_arr_result
            else:
                numpy_arr = np.frombuffer(raw_data, _NP_DTYPES[current_format])
                numpy_arr_result = numpy_arr.reshape(-1, 1)
                return numpy_arr_result
        else:
            raise ValueError("Unsupported Format")

    def save_wav(self, wav_name):
        """
        Saves the audio recording to a wav file. File can be played.
        """
        def clamp():
            """
            clamps float32 to int16 values and returns a byte string of the format
            """
            numeric_samples = self.get_numpy()
            np.clip(numeric_samples, -1.0, 1.0, out=numeric_samples)
            numeric_samples = numeric_samples * 32767.0
            numeric_samples = np.round(numeric_samples)
            int16_samples = numeric_samples.astype(np.int16)
            return int16_samples.tobytes()

        def find_latest_filenumber():
            """
            Finds the max file number in the directory recordings
            """
            current_wd = os.getcwd()
            recordings_dir = os.path.join(current_wd, "recordings")
            files = os.listdir(recordings_dir)
            max_number = 0
            for f in files:
                if f.endswith(".wav") and f.startswith(self.audio_config.default_filename_prefix):
                    match = re.search(rf'(?<={re.escape(self.audio_config.default_filename_prefix)}_)\d+', f)
                    if match:
                        extracted_part = match.group(0)
                        max_number = max(max_number, int(extracted_part) + 1)
                    else:
                        max_number = max(max_number, max_number + 1)
            return max_number

        if self.is_recording():
            return ("recording in session")
        current_channels = self.audio_config.channels
        current_format = self.audio_config.sample_format
        current_sample_rate = self.audio_config.rate

        current_audio_bytes = self.get_raw_bytes(self.frames)

        output_dir = self.audio_config.output_dir
        file_name_prefix = self.audio_config.default_filename_prefix
        if not self.audio_config.auto_increment:
            filename_wav_format = output_dir + "/" + wav_name + ".wav"
        else:
            latest_filenumber = find_latest_filenumber()
            if latest_filenumber == 0:
                latest_filenumber = "_00" + str(latest_filenumber)
                filename_wav_format = (output_dir + "/" + file_name_prefix + latest_filenumber
                                       + ".wav")
            else:
                if 10 <= latest_filenumber < 100:
                    latest_filenumber = "_0" + str(latest_filenumber)
                    filename_wav_format = (output_dir + "/" + file_name_prefix + latest_filenumber
                                           + ".wav")
                elif 1 <= latest_filenumber < 10:
                    latest_filenumber = "_00" + str(latest_filenumber)
                    filename_wav_format = (output_dir + "/" + file_name_prefix + latest_filenumber +
                                           ".wav")

        with wave.open(filename_wav_format, "wb") as wf:
            wf.setnchannels(current_channels)

            if current_format == "float32":
                if len(current_audio_bytes) != 0:
                    current_audio_bytes = clamp()
                block_align = current_channels * 2
                byte_rate = current_sample_rate * block_align
                remainder_frame_bytes = len(current_audio_bytes) % block_align
                if remainder_frame_bytes != 0:
                    current_audio_bytes = current_audio_bytes[:-remainder_frame_bytes]
                wf.setsampwidth(2)

            elif current_format == "int16":
                block_align = current_channels * 2
                byte_rate = current_sample_rate * block_align
                remainder_frame_bytes = len(current_audio_bytes) % block_align
                if remainder_frame_bytes != 0:
                    current_audio_bytes = current_audio_bytes[:-remainder_frame_bytes]
                wf.setsampwidth(2)
            elif (current_format == "int32"):
                block_align = current_channels * 4
                byte_rate = current_sample_rate * block_align
                remainder_frame_bytes = len(current_audio_bytes) % block_align
                if remainder_frame_bytes != 0:
                    current_audio_bytes = current_audio_bytes[:-remainder_frame_bytes]
                wf.setsampwidth(4)

            wf.setframerate(current_sample_rate)
            wf.writeframes(current_audio_bytes)
