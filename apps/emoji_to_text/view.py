""""
Creates the GUI for the emoji to text translation
"""
import os.path
from PySide6.QtWidgets import QGridLayout, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QPushButton, \
    QScrollArea, QVBoxLayout, \
    QWidget
from PySide6.QtCore import Qt


class EmojiToTextView(QMainWindow):
    """Class representing the gui for the emoji to text app"""

    def __init__(self):
        super().__init__()
        BASE_PATH = os.path.dirname(__file__)

        # central widget housing the main parts of the app
        central_widget = QWidget()
        central_widget.setObjectName("central")
        self.setCentralWidget(central_widget)
        central_widget_layout = QGridLayout()
        central_widget.setLayout(central_widget_layout)
        central_widget.setAttribute(Qt.WA_StyledBackground, True)

        background_image_path = os.path.join(BASE_PATH, "emoji-background.jpg")
        central_widget.setStyleSheet(f"""
        QWidget#central {{
            background-image: url("{background_image_path}");
        }}
        QLineEdit{{
            border: 1px solid black;
        }}
        QLabel#Title{{
            font-size: 18px;
            font-weight: bold;
            color: blue;
            background-color: lightgrey;
        }}
        QLabel#Box{{
            border: 1px solid black;
            background-color: lightgrey;
        }}
        QPushButton {{
            background-color: black;
        }}
        QPushButton:hover{{
                background-color: #f0f0f0;
            }}
        QPushButton:pressed{{
            background-color: #d0d0d0;
        }}
        
        """)

        # input message
        input_message_layout = QVBoxLayout()
        input_message_title = QLabel("Your Input")
        input_message_title.setObjectName("Title")
        second_inner_layout = QHBoxLayout()
        self.input_message = QLineEdit()
        self.input_message.setMaxLength(100)
        self.input_message.setPlaceholderText("Your text can contain emojis or not")
        self.translate_button = QPushButton("Translate")
        second_inner_layout.addWidget(self.input_message)
        second_inner_layout.addWidget(self.translate_button)
        input_message_layout.addWidget(input_message_title)
        input_message_layout.addSpacing(5)
        input_message_layout.addLayout(second_inner_layout)

        # first letter text box
        first_letter_layout = QHBoxLayout()
        first_letter_title = QLabel("Emoji First Letter")
        first_letter_title.setObjectName("Title")
        self.first_letter_textbox = QLabel("")
        self.first_letter_textbox.setObjectName("Box")
        self.first_letter_textbox.setWordWrap(True)
        first_letter_scroll = QScrollArea()
        first_letter_scroll.setWidgetResizable(True)
        first_letter_scroll.setWidget(self.first_letter_textbox)
        first_letter_layout.addWidget(first_letter_title)
        first_letter_layout.addSpacing(5)
        first_letter_layout.addWidget(first_letter_scroll)

        # middle letter text box
        middle_letter_layout = QHBoxLayout()
        middle_letter_title = QLabel("Emoji Middle Letter")
        middle_letter_title.setObjectName("Title")
        self.middle_letter_textbox = QLabel("")
        self.middle_letter_textbox.setObjectName("Box")
        self.middle_letter_textbox.setWordWrap(True)
        middle_letter_scroll = QScrollArea()
        middle_letter_scroll.setWidgetResizable(True)
        middle_letter_scroll.setWidget(self.middle_letter_textbox)
        middle_letter_layout.addWidget(middle_letter_title)
        middle_letter_layout.addSpacing(5)
        middle_letter_layout.addWidget(middle_letter_scroll)

        # last letter text box
        last_letter_layout = QHBoxLayout()
        last_letter_title = QLabel("Emoji Last Letter")
        last_letter_title.setObjectName("Title")
        self.last_letter_textbox = QLabel("")
        self.last_letter_textbox.setObjectName("Box")
        self.last_letter_textbox.setWordWrap(True)
        last_letter_scroll = QScrollArea()
        last_letter_scroll.setWidgetResizable(True)
        last_letter_scroll.setWidget(self.last_letter_textbox)
        last_letter_layout.addWidget(last_letter_title)
        last_letter_layout.addSpacing(5)
        last_letter_layout.addWidget(last_letter_scroll)

        # binary version text box
        binary_version_layout = QHBoxLayout()
        binary_version_title = QLabel("Binary version of the text")
        binary_version_title.setObjectName("Title")
        self.binary_textbox = QLabel("")
        self.binary_textbox.setObjectName("Box")
        self.binary_textbox.setWordWrap(True)
        binary_scrollArea = QScrollArea()
        binary_scrollArea.setWidgetResizable(True)
        binary_scrollArea.setWidget(self.binary_textbox)
        binary_version_layout.addWidget(binary_version_title)
        binary_version_layout.addSpacing(5)
        binary_version_layout.addWidget(binary_scrollArea)

        # full meaning textbox
        full_meaning_layout = QHBoxLayout()
        full_meaning_title = QLabel("Full meaning")
        full_meaning_title.setObjectName("Title")
        self.full_meaning_textbox = QLabel("")
        self.full_meaning_textbox.setObjectName("Box")
        self.full_meaning_textbox.setWordWrap(True)
        full_meaning_scroll_area = QScrollArea()
        full_meaning_scroll_area.setWidgetResizable(True)
        full_meaning_scroll_area.setWidget(self.full_meaning_textbox)
        full_meaning_layout.addWidget(full_meaning_title)
        full_meaning_layout.addSpacing(5)
        full_meaning_layout.addWidget(full_meaning_scroll_area)

        # arranging the different layouts
        central_widget_layout.addLayout(input_message_layout, 0, 1, 2, 10)
        central_widget_layout.addLayout(first_letter_layout, 3, 1, 2, 10)
        central_widget_layout.addLayout(middle_letter_layout, 6, 1, 2, 10)
        central_widget_layout.addLayout(last_letter_layout, 9, 1, 2, 10)
        central_widget_layout.addLayout(binary_version_layout, 12, 1, 2, 10)
        central_widget_layout.addLayout(full_meaning_layout, 15, 1, 2, 10)
