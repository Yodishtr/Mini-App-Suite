"""
Creates the specific UI for rock paper scissors.
Utilizes the common/ui/__init__ as a wrapper to keep fonts, colors and styles
consistent across the app.

"""
import os.path
from pathlib import Path

from PySide6.QtCore import QEasingCurve, QParallelAnimationGroup, QPoint, QPropertyAnimation, QRect, \
    QSequentialAnimationGroup, QSize, Qt, Slot
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QGraphicsOpacityEffect, QGridLayout, QHBoxLayout, QLabel, QMainWindow, \
    QPushButton, QSpinBox, \
    QVBoxLayout, QWidget


class GameView(QMainWindow):
    """A class that represents the main game window"""

    def __init__(self):
        """View Initialization"""
        BASE_PATH = os.path.dirname(__file__)
        super().__init__()
        self.setWindowTitle("Welcome to the Rock-Paper-Scissors Game!")
        self.setGeometry(400, 400, 800, 600)

        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_layout = QGridLayout(central_widget)
        background_image = os.path.join(BASE_PATH, "RPS_background.jpg")
        central_widget.setStyleSheet("background-image: url(" + background_image +
                                     ");" +
                                     "background-size: cover;")

        # Difficulty settings
        # maybe move this and the choosing the number of rounds in a preliminary window
        # where you can then choose the number of rounds first then have it switch to
        # game view window
        user_choice_layout = QHBoxLayout()
        self.easy_difficulty_button = QPushButton("Easy")
        self.medium_difficulty_button = QPushButton("Medium")
        self.hard_difficulty_button = QPushButton("Hard")

        # set number of rounds
        self.roundsChosen = QSpinBox()
        self.roundsChosen.setMinimum(1)
        self.roundsChosen.setMaximum(1000)
        self.roundsChosen.setSingleStep(1)
        self.roundsChosen.setSuffix(" Rounds")

        user_choice_layout.addWidget(self.easy_difficulty_button)
        user_choice_layout.addSpacing(5)
        user_choice_layout.addWidget(self.medium_difficulty_button)
        user_choice_layout.addSpacing(5)
        user_choice_layout.addWidget(self.hard_difficulty_button)
        user_choice_layout.addSpacing(5)
        user_choice_layout.addWidget(self.roundsChosen)

        # Set moves Button
        # add an animation when the move is selected
        moves_layout = QHBoxLayout()
        self.rock_button = QPushButton("Rock")
        self.paper_button = QPushButton("Paper")
        self.scissor_button = QPushButton("Scissors")
        self.rock_button.setEnabled(False)
        self.paper_button.setEnabled(False)
        self.scissor_button.setEnabled(False)
        # add icons to the moves button
        rock_icon = os.path.join(BASE_PATH, "hand.png")
        self.rock_button.setIcon(QIcon(rock_icon))

        paper_icon = os.path.join(BASE_PATH, "hand-paper.png")
        self.paper_button.setIcon(QIcon(paper_icon))

        scissors_icon = os.path.join(BASE_PATH, "scissors.png")
        self.scissor_button.setIcon(QIcon(scissors_icon))

        moves_layout.addWidget(self.rock_button)
        moves_layout.addWidget(self.paper_button)
        moves_layout.addWidget(self.scissor_button)

        # Menu Labels
        menu_layout = QHBoxLayout()

        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_on_click)

        difficulty_layout = QVBoxLayout()
        difficulty_title = QLabel("Difficulty")
        self.difficulty_display = QLabel("")
        difficulty_layout.addWidget(difficulty_title)
        difficulty_layout.addWidget(self.difficulty_display)

        total_rounds_layout = QVBoxLayout()
        total_rounds_title = QLabel("Total rounds")
        self.total_rounds_display = QLabel()
        total_rounds_layout.addWidget(total_rounds_title)
        total_rounds_layout.addWidget(self.total_rounds_display)

        rounds_played_layout = QVBoxLayout()
        rounds_played_title = QLabel("Rounds Played: ")
        self.rounds_played_display = QLabel()
        rounds_played_layout.addWidget(rounds_played_title)
        rounds_played_layout.addWidget(self.rounds_played_display)

        player_score_layout = QVBoxLayout()
        player_score_title = QLabel("Player Score")
        self.player_score_display = QLabel()
        player_score_layout.addWidget(player_score_title)
        player_score_layout.addWidget(self.player_score_display)

        computer_score_layout = QVBoxLayout()
        computer_score_title = QLabel("Computer Score")
        self.computer_score_display = QLabel()
        computer_score_layout.addWidget(computer_score_title)
        computer_score_layout.addWidget(self.computer_score_display)

        menu_layout.addLayout(difficulty_layout)
        menu_layout.addSpacing(20)
        menu_layout.addLayout(total_rounds_layout)
        menu_layout.addSpacing(20)
        menu_layout.addLayout(rounds_played_layout)
        menu_layout.addSpacing(20)
        menu_layout.addLayout(player_score_layout)
        menu_layout.addSpacing(20)
        menu_layout.addLayout(computer_score_layout)
        menu_layout.addSpacing(20)
        menu_layout.addWidget(self.reset_button)

        # computer move layout (to show user what move the computer made)
        computer_move_layout = QVBoxLayout()
        self.computer_move_label = QLabel("Computer Move: ")
        self.computer_move_label_image = QLabel()
        self.computer_move_label_image.setMinimumSize(240, 240)
        self.computer_move_label_image.setAlignment(Qt.AlignCenter)
        computer_move_layout.addWidget(self.computer_move_label)
        computer_move_layout.addSpacing(10)
        computer_move_layout.addWidget(self.computer_move_label_image)

        # result display
        final_result_layout = QHBoxLayout()
        self.result_label_title = QLabel("The final result is: ")
        self.result_label_display = QLabel("")
        final_result_layout.addWidget(self.result_label_title)
        final_result_layout.addSpacing(5)
        final_result_layout.addWidget(self.result_label_display)

        # Central layout adding other layouts
        central_layout.addLayout(menu_layout, 0, 0, 2, 6)
        central_layout.addLayout(user_choice_layout, 1, 0, 1, 6)
        self.animation_widget = QWidget()
        self.animation_widget.setFixedSize(240, 240)
        self.animation_widget.setStyleSheet("border: 2px dashed gray")
        central_layout.addWidget(self.animation_widget, 2, 1)
        self._throw_label = None
        self._opacity = None
        self._anim_group = None
        # create an animation widget with fix width and height and which will
        # have a layout (maybe QVBoxLayout) with a Qlabel containing the image
        # and then add the widget here
        central_layout.addLayout(moves_layout, 5, 1, 2, 6)
        central_layout.addLayout(computer_move_layout, 6, 1, 5, 5)
        central_layout.addLayout(final_result_layout, 12, 1, 1, 5)

    @Slot
    def reset_on_click(self):
        """
        Controller uses this to activate the reset for the game
        :return: None
        """
        self.update_rounds_played("0")
        self.update_player_score("0")
        self.update_computer_score("0")
        self.easy_difficulty_button.setEnabled(True)
        self.medium_difficulty_button.setEnabled(True)
        self.hard_difficulty_button.setEnabled(True)
        self.move_buttons_disabled()

    def update_difficulty(self, level: str):
        """
        Controller uses this to update the difficulty set by the player
        :param level:
        """
        self.difficulty_display.setText(level)

    def update_total_rounds(self, total_rounds):
        """
        Controller uses this to update the total number of rounds selected by the player
        :param total_rounds:
        """
        self.total_rounds_display.setText(total_rounds)

    def update_rounds_played(self, played: str):
        """
        Controller uses this to update the  rounds played till now in the game.
        :param played:
        """
        self.rounds_played_display.setText(played)

    def update_player_score(self, player_score: str):
        """
        Controller uses this to update the score board with the player's current score
        :param player_score:
        """
        self.player_score_display.setText(player_score)

    def update_computer_score(self, computer_score: str):
        """
        Controller uses this to update the score board with the computer's current score
        :param computer_score:
        """
        self.computer_score_display.setText(computer_score)

    def move_buttons_enabled(self):
        """
        Enables the move buttons if they have been disabled
        """
        if (not self.rock_button.isEnabled()) and (not self.paper_button.isEnabled()) and \
                (not self.paper_button.isEnabled()):
            self.rock_button.setEnabled(True)
            self.paper_button.setEnabled(True)
            self.scissor_button.setEnabled(True)

    def move_buttons_disabled(self):
        """
        Disables the move buttons if they have been enabled
        """
        if (self.rock_button.isEnabled() and self.paper_button.isEnabled() and
                self.scissor_button.isEnabled()):
            self.rock_button.setEnabled(False)
            self.paper_button.setEnabled(False)
            self.scissor_button.setEnabled(False)

    def enable_difficulty_buttons(self):
        """
        Enables the difficulty buttons.
        """
        if (not self.easy_difficulty_button.isEnabled() and
                not self.medium_difficulty_button.isEnabled() and
                not self.hard_difficulty_button.isEnabled()):
            self.easy_difficulty_button.setEnabled(True)
            self.medium_difficulty_button.setEnabled(True)
            self.hard_difficulty_button.setEnabled(True)

    def disable_difficulty_button(self):
        """
        Disables the difficult buttons.
        """
        if (self.easy_difficulty_button.isEnabled() and self.medium_difficulty_button.isEnabled()
                and self.hard_difficulty_button.isEnabled()):
            self.easy_difficulty_button.setEnabled(False)
            self.medium_difficulty_button.setEnabled(False)
            self.hard_difficulty_button.setEnabled(False)

    def get_rounds_chosen(self):
        """
        Returns the number of rounds chosen by the player
        """
        return self.roundsChosen.value()

    def move_animation(self, move_selected):
        """
        Animates the move selected by the user in the animation_widget space.
        :param move_selected:
        """
        if self._anim_group is not None:
            try:
                self._anim_group.stop()
            except Exception:
                pass
            self._anim_group = None

        self.move_buttons_disabled()
        button_map = {
            "ROCK": self.rock_button,
            "PAPER": self.paper_button,
            "SCISSORS": self.scissor_button
        }
        source_button = button_map[move_selected]
        if source_button is None:
            self.move_buttons_disabled()
            return

        icon = source_button.icon()
        if icon.isNull():
            self.move_buttons_enabled()
            return

        if self._throw_label is None:
            self._throw_label = QLabel(self.animation_widget)
            self._throw_label.setAttribute(Qt.WA_TransparentForMouseEvents, True)
            self._throw_label.setScaledContents(True)

        self._throw_label.raise_()
        self._throw_label.show()

        margin = 0
        end_rect = self.animation_widget.contentsRect().adjusted(margin, margin, -margin, -margin)

        target_size = QSize(max(1, end_rect.width()), max(1, end_rect.height()))
        pixmap = icon.pixmap(target_size)
        self._throw_label.setPixmap(pixmap)

        button_center_global = source_button.mapToGlobal(source_button.rect().center())
        start_center = self.animation_widget.mapFromGlobal(button_center_global)

        start_scale = 0.35
        w0 = max(1, int(end_rect.width() * start_scale))
        h0 = max(1, int(end_rect.width() * start_scale))
        start_rect = QRect(
            QPoint(start_center.x() - w0 // 2, start_center.y() - h0 // 2),
            QSize(w0, h0)
        )
        start_rect = start_rect.intersected(self.animation_widget.rect().adjusted(-w0, -h0, w0, h0))
        self._throw_label.setGeometry(start_rect)

        if self._opacity is None:
            self._opacity = QGraphicsOpacityEffect(self._throw_label)
        self._throw_label.setGraphicsEffect(self._opacity)
        self._opacity.setOpacity(0.0)

        duration_travel = 300
        duration_squash = 90
        duration_rebound = 140

        anim_travel = QPropertyAnimation(self._throw_label, b"geometry")
        anim_travel.setDuration(duration_travel)
        anim_travel.setStartValue(start_rect)
        anim_travel.setEndValue(end_rect)
        anim_travel.setEasingCurve(QEasingCurve.OutQuart)

        anim_fade = QPropertyAnimation(self._opacity, b"opacity")
        anim_fade.setDuration(duration_travel)
        anim_fade.setStartValue(0.0)
        anim_fade.setEndValue(1.0)
        anim_fade.setEasingCurve(QEasingCurve.OutCubic)

        travel_group = QParallelAnimationGroup()
        travel_group.addAnimation(anim_travel)
        travel_group.addAnimation(anim_fade)

        squeeze_x = int(end_rect.width() * 0.05)
        squeeze_y = int(end_rect.height() * 0.05)
        squash_rect = QRect(
            end_rect.left() - squeeze_x,
            end_rect.top() - squeeze_y,
            end_rect.width() + 2 * squeeze_x,
            end_rect.height() + 2 * squeeze_y
        )

        anim_squash = QPropertyAnimation(self._throw_label, b"geometry")
        anim_squash.setDuration(duration_squash)
        anim_squash.setStartValue(end_rect)
        anim_squash.setEndValue(squash_rect)
        anim_squash.setEasingCurve(QEasingCurve.InQuad)

        anim_rebound = QPropertyAnimation(self._throw_label, b"geometry")
        anim_rebound.setDuration(duration_rebound)
        anim_rebound.setStartValue(squash_rect)
        anim_rebound.setEndValue(end_rect)
        anim_rebound.setEasingCurve(QEasingCurve.OutBack)

        seq = QSequentialAnimationGroup(self)
        seq.addAnimation(travel_group)
        seq.addAnimation(anim_squash)
        seq.addAnimation(anim_rebound)

        def _on_finished():
            self._anim_group = None
            self.move_buttons_enabled()

        seq.finished.connect(_on_finished)
        self._anim_group = seq
        seq.start()
