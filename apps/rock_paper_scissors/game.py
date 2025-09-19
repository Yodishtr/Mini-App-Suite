from enum import Enum
"""
This contains the pure logic of the game such as the current state and
the game rules etc.

"""


"""This is an inner class to represent the move of a player"""
class Move(Enum):
    ROCK = "rock"
    PAPER = "paper"
    SCISSORS = "scissors"

    def beats(self, other):
        """Checks the winning move from the two inputs"""
        if self == Move.ROCK and other == Move.SCISSORS:
            return True
        elif self == Move.SCISSORS and other == Move.PAPER:
            return True
        elif self == Move.PAPER and other == Move.ROCK:
            return True
        else:
            return False


class EventEmitter:

    """
    This class is an Event Emitter that allows the game to send payloads of data to the ui via
    the app
    """

    def __init__(self):
        self.my_events = {}

    def on(self, event, handler):
        """Sets up event's handler"""
        if event not in self.my_events:
            self.my_events[event] = []
        self.my_events[event].append(handler)

    def emit(self, event, payloadData=None):
        """Assigned handler emits payload data to ui via handler return format"""
        if event in self.my_events:
            for handler in self.my_events[event]:
                handler(payloadData)


class Game:

    """This class represents the game logic for rock paper scissors"""
    def __init__(self, difficulty: str, num_round=5):
        """Maybe add a storage device as an argument to the game."""
        self.difficulty = difficulty
        self.numRounds = num_round
        self.currentRound = 0
        self.playerScore = 0
        self.computerScore = 0

    def start(self):
        """Can make it emit an RPS event? so that changes can be propagated to UI"""
        self.currentRound = 0
        self.computerScore = 0
        self.playerScore = 0

    def reset(self):
        """resets the game"""
        self.currentRound = 0
        self.computerScore = 0
        self.playerScore = 0

    def legalMove(self):
        """Returns a list of the allowed moves"""
        return [Move.ROCK, Move.PAPER, Move.SCISSORS]

    def playRound(self, playerMove: Move):
        """Returns a small ui friendly round result (could be a dict) and also emits
        an event to allow ui to render. app.py extracts user input and creates a Move object which
        is passed to this method.
        """
        if playerMove not in self.legalMove():
            return "Invalid input"
        else:
            if self.difficulty == "easy":
                result = self.easyCompMove(playerMove)
                return result
            elif self.difficulty == "medium":
                result = self.mediumCompMove(playerMove)
                return result
            elif self.difficulty == "hard":
                result = self.hardCompMove(playerMove)
                return result


    def easyCompMove(self, playerMove):
        preset = {1: Move.ROCK, 2: Move.PAPER, 3: Move.SCISSORS}


    def mediumCompMove(self, playerMove):
        pass


    def hardCompMove(self, playerMove):
        pass
