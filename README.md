Python Mini Projects Suite 🎮🛠️

A collection of small Python applications—games and utilities—built with a shared structure and GUI powered by PySimpleGUI.
This project demonstrates modular design: each mini-app is self-contained but shares common utilities for configuration, storage, and UI themes.

📂 Project Structure
python-mini-suite/
├─ README.md
├─ requirements.txt
├─ scripts/
│  └─ run.py             # launcher to select and start apps
├─ assets/               # shared icons, sounds, fonts
├─ data/
│  ├─ saved/             # user saves, scores, history (gitignored)
│  └─ samples/           # sample resources
├─ common/               # reusable utilities
│  ├─ ui/                # GUI components, themes
│  ├─ core/              # config, storage, audio, screen utils
│  └─ logging.py
├─ apps/
│  ├─ number_guessing/
│  ├─ word_guessing/
│  ├─ hangman/
│  ├─ twenty_one/
│  ├─ rock_paper_scissors/
│  ├─ emoji_to_text/
│  ├─ voice_recorder/
│  ├─ screen_recorder/
│  └─ mastermind/
└─ tests/
   ├─ common/
   └─ apps/


Each app follows a mini-package format:

apps/<app_name>/
├─ app.py         # GUI entrypoint
├─ game.py        # pure logic/state (testable)
├─ config.yaml    # default settings
├─ assets/        # app-specific resources
└─ tests/         # unit tests for game logic

📜 Included Sub-Projects

Number Guessing Game – Guess the secret number with hints.

Word Guessing Game – Wordle-style guessing with feedback.

Hangman Game – Classic letter guessing with limited lives.

21 Number Game – Mathematical take-away game against CPU.

Rock Paper Scissors – Classic or extended (Lizard/Spock) rules.

Emoji → Text Converter – Replace emojis with text names.

Voice Recorder – Record audio, save as WAV/MP3.

Screen Recorder – Capture screen (and optionally mic) to video.

Mastermind Game – Deduce a hidden code with color/peg feedback.

⚙️ Requirements

Core: Python 3.10+

PySimpleGUI
 (GUI)

pytest (testing)

Optional (media apps only):

sounddevice / pyaudio – audio recording

mss – screen capture

imageio-ffmpeg or opencv-python – video encoding

pyperclip – clipboard support

Install core dependencies:

pip install -r requirements.txt


For recorders:

pip install sounddevice mss imageio-ffmpeg

🚀 Usage

Launch the suite

python scripts/run.py


This opens a launcher window listing all available apps.

Run a single app

python -m apps.number_guessing.app

✅ Requirements per Sub-Project
Games (Number, Word, Hangman, 21, RPS, Mastermind)

Configurable difficulty (range, attempts, rules).

Persistent stats/history saved in data/saved/.

GUI with input controls, score display, and replay button.

Logic isolated in game.py (testable without GUI).

Emoji to Text

Input/output text panels.

Option to export to file or clipboard.

Handles ZWJ sequences (flags, skin tones).

Voice Recorder

Record, pause/resume, stop.

Save WAV/MP3 files with metadata.

Device selection + peak meter.

Screen Recorder

Capture full screen or region.

FPS and output format settings.

Optional microphone audio merge.

🧪 Testing

Run unit tests (logic only):

pytest tests/

