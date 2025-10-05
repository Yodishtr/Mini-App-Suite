"""
Creates the GUI for the number guessing game.
"""
from PySide6.QtWidgets import QGridLayout, QMainWindow, QWidget
import yaml


class NumberGameView(QMainWindow):
    """The class representing the GUI for the number guessing app."""

    def __init__(self):
        """Initializes the view for the number game view"""
        super().__init__()
        self.data = self._load_yaml()

        # central widget
        central_widget = QWidget()
        central_widget.setObjectName("CENTRAL")
        self.setCentralWidget(central_widget)
        central_widget_layout = QGridLayout()
        central_widget.setLayout(central_widget_layout)

        if self.data:
            background_image = self.data[BACKGROUND]





    def _load_yaml(self):
        """Loads the data from the yaml"""
        try:
            with open('config.yaml', 'r') as file:
                result = yaml.safe_load(file)
                return result
        except FileNotFoundError:
            print("No config.yaml found")
            return None
        except yaml.YAMLError as e:
            print("Yaml error: " + str(e))
            return None
