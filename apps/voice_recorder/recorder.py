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


class RecordingInSession(Exception):
    """
    Exceptions raised when operations are being done on frames while recording is being done
    """
    def __init__(self, message="Recording is in session"):
        self.message = message
        super().__init__(self.message)


class PlayRecordingInSession(Exception):
    """
    Exception raised when trying to press play button while playing is being done
    """
    def __init__(self, message="Playing in session"):
        self.message = message
        super().__init__(self.message)

class NoRecordingAvailable(Exception):
    """
    Exception raised when trying to play an empty self.frame.
    """
    def __init__(self, message="No current recordings to be played"):
        self.message = message
        super().__init__(self.message)


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

        # enables us to check if the recording is done playing now
        self.playback_done = threading.Event()

        # enables us to check if the recording is currently paused, stopped or playing
        self.play_status = "stopped"

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
            raise RecordingInSession

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

    def is_in_playing(self):
        """
        Checks the thread where the audio is currently being played.
        Returns True if a recording is being played and False otherwise
        """
        return self.playing.is_set()

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
            current_wd = os.path.dirname(os.path.abspath(__file__))
            recordings_dir = os.path.join(current_wd, self.audio_config.output_dir)
            if not os.path.isdir(recordings_dir):
                os.mkdir(recordings_dir)
            files = os.listdir(recordings_dir)
            max_number = 0
            for f in files:
                if (f.endswith(".wav") and f.startswith(f"{self.audio_config.default_filename_prefix}_")):
                    match = re.search(rf'(?<={re.escape(self.audio_config.default_filename_prefix)}_)\d+', f)
                    if match:
                        extracted_part = match.group(0)
                        max_number = max(int(extracted_part), max_number)

            return max_number + 1

        if self.is_recording():
            raise RecordingInSession()
        current_channels = self.audio_config.channels
        current_format = self.audio_config.sample_format
        current_sample_rate = self.audio_config.rate

        current_audio_bytes = self.get_raw_bytes(self.frames)

        current_wd = os.path.dirname(os.path.abspath(__file__))
        output_dir = os.path.join(current_wd, self.audio_config.output_dir)
        file_name_prefix = self.audio_config.default_filename_prefix
        if not self.audio_config.auto_increment:
            if not os.path.isdir(output_dir):
                os.mkdir(output_dir)
            if wav_name.endswith(".wav"):
                wav_name = wav_name[:-4]
            filename_wav_format = os.path.join(output_dir, (wav_name + ".wav"))
        else:
            latest_filenumber = find_latest_filenumber()
            left_padded_filenumber = str(latest_filenumber).zfill(3)
            file_name = file_name_prefix + "_" + left_padded_filenumber + ".wav"
            filename_wav_format = os.path.join(output_dir, file_name)

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

    def _start_playback_monitor(self):
        """
        A lightweight background thread that clears up after natural completion
        """
        if getattr(self, "_playback_monitor_thread",
                   None) and self._playback_monitor_thread.is_alive():
            return
        self._playback_monitor_thread = threading.Thread(
            target=self._playback_monitor_loop, daemon=True
        )
        self._playback_monitor_thread.start()

    def _playback_monitor_loop(self):
        """
        Waits for playback to start (self.playing set), then waits for natural completion
        (self.playback_done set by the callback). When that happens, it performs teardown
        on the main side (not inside the callback).
        """
        while True:
            # wait until playing actually starts
            self.playing.wait()
            # wait until playback_done signals completion
            self.playback_done.wait()
            # at this point the playback finished naturally
            try:
                if self.out_stream is not None:
                    try:
                        self.out_stream.stop_stream()
                    except Exception:
                        print("Fuck this")
                    try:
                        self.out_stream.close()
                    except Exception:
                        print("Fuck this again")
                    self.out_stream = None
            finally:
                self.play_status = "stopped"
                self.playing.clear()
                with self.lock:
                    self.play_pos = 0
                self.playback_done.clear()

    def play_audio(self):
        """
        Plays the wav file if provided, otherwise it will just play directly from the current
        self.frames which is being recorded
        """
        def _callback(data_in, frame_count, time_info, status_flag):
            if self.is_in_playing():
                bytes_needed = frame_count * current_channel_number * bytes_per_sample
                with self.lock:
                    chunk = recorded_bytes[self.play_pos: self.play_pos + bytes_needed]
                    self.play_pos += len(chunk)
                    if len(chunk) == bytes_needed:
                        return (chunk, pyaudio.paContinue)
                    elif len(chunk) < bytes_needed:
                        difference = bytes_needed - len(chunk)
                        padded_zeroes = [0] * difference
                        chunk += bytes(padded_zeroes)
                        self.playback_done.set()
                        return (chunk, pyaudio.paComplete)

            else:
                bytes_needed = frame_count * current_channel_number * bytes_per_sample
                silence_bytes = bytes([0] * bytes_needed)
                return (silence_bytes, pyaudio.paContinue)

        if len(self.frames) == 0:
            raise NoRecordingAvailable

        if self.play_status == "playing":
            raise PlayRecordingInSession()

        current_format_str = self.audio_config.sample_format
        if current_format_str == "int16":
            bytes_per_sample = 2
        elif (current_format_str == "int32" or current_format_str == "float32"):
            bytes_per_sample = 4

        current_rate = self.audio_config.rate
        current_format = _SAMPLE_FORMAT[current_format_str]
        current_channel_number = self.audio_config.channels
        bytes_per_frame = current_channel_number * bytes_per_sample
        recorded_bytes = self.get_raw_bytes(self.frames)
        if self.play_pos % bytes_per_frame != 0:
            self.play_pos -= self.play_pos % bytes_per_frame
        self.out_stream = self.audio_system.open(format=current_format,
                                                 channels=current_channel_number,
                                                 rate=current_rate,
                                                 output=True,
                                                 frames_per_buffer=self.audio_config.chunk,
                                                 stream_callback=_callback)

        self.playing.set()
        self.play_status = "playing"
        self.playback_done.clear()
        self.out_stream.start_stream()
        self._start_playback_monitor()

    def pause_playing(self):
        """
        Pauses the playing of a recording
        """
        if not self.play_status == "playing":
            return
        self.play_status = "paused"
        self.playing.clear()
        self.out_stream.stop_stream()
        self.out_stream.close()
        self.playback_done.set()
        self.out_stream = None

    def stop_playing(self):
        """
        Stops the playing of a recording and resets the playhead position to the start of the
        recording
        """
        if self.play_status == "stopped":
            with self.lock:
                self.play_pos = 0
        else:
            with self.lock:
                self.play_pos = 0
                self.playing.clear()
                self.out_stream.stop_stream()
                self.out_stream.close()
                self.out_stream = None
                self.playback_done.set()
                self.play_status = "stopped"
