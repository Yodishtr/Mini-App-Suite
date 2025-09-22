from enum import Enum
from random import randint
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
        if ((self == Move.ROCK and other == Move.SCISSORS) or
                (self == Move.SCISSORS and other == Move.PAPER) or
                (self == Move.PAPER and other == Move.ROCK)):
            return ("Computer Wins")
        elif ((self == Move.PAPER and other == Move.PAPER) or
              (self == Move.ROCK and other == Move.ROCK) or
              (self == Move.SCISSORS and other == Move.SCISSORS)):
            return ("Draw")
        else:
            return ("Player Wins")


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
    def __init__(self, difficulty: str, num_round):
        """Maybe add a storage device as an argument to the game."""
        self.difficulty = difficulty
        self.numRounds = num_round
        self.currentRound = 0
        self.playerScore = 0
        self.computerScore = 0
        self.computerMove = None
        self.frequencyAnalysis = {Move.ROCK: 0, Move.PAPER: 0, Move.SCISSORS: 0}

    def start(self):
        """Can make it emit an RPS event? so that changes can be propagated to UI"""
        self.currentRound = 0
        self.computerScore = 0
        self.playerScore = 0
        self.computerMove = None
        for key in self.frequencyAnalysis:
            self.frequencyAnalysis[key] = 0

    def reset(self):
        """resets the game"""
        self.currentRound = 0
        self.computerScore = 0
        self.playerScore = 0
        self.computerMove = None
        for key in self.frequencyAnalysis:
            self.frequencyAnalysis[key] = 0

    def legalMove(self):
        """Returns a list of the allowed moves"""
        return [Move.ROCK, Move.PAPER, Move.SCISSORS]

    def playRound(self, playerMove: Move):
        """Returns a small ui friendly round result (could be a dict) and also emits
        an event to allow ui to render. app.py extracts user input and creates a Move object which
        is passed to this method.
        """
        self.frequencyAnalysis[playerMove] += 1
        if playerMove not in self.legalMove():
            return "Invalid input"
        else:
            if self.difficulty == "easy":
                result = self.easyCompMove(playerMove)
                return result
            elif self.difficulty == "medium":
                self.computerMove = self.mediumCompMove(playerMove)
                result = self.computerMove.beats(playerMove)
                return result
            elif self.difficulty == "hard":
                self.computerMove = self.hardCompMove(playerMove)
                result = self.computerMove.beats(playerMove)
                return result

    def easyCompMove(self, playerMove):
        """Computer makes a random move"""
        preset = {1: Move.ROCK, 2: Move.PAPER, 3: Move.SCISSORS}
        computerChoice = randint(1, 3)
        currentComputerMove = preset[computerChoice]
        self.computerMove = currentComputerMove
        return self.computerMove.beats(playerMove)

    def mediumCompMove(self, playerMove):
        """
        Makes a computer move based on the most used player move
        :param playerMove:
        :return: computer move
        """
        if sum(self.frequencyAnalysis.values()) == 0:
            return self.easyCompMove(playerMove)
        else:
            mostUsed = 0
            playerMostUsed = None
            for key in self.frequencyAnalysis:
                currentFrequency = self.frequencyAnalysis[key]
                if currentFrequency > mostUsed:
                    mostUsed = currentFrequency
                    playerMostUsed = key
            if playerMostUsed == Move.PAPER:
                return Move.SCISSORS
            elif playerMostUsed == Move.ROCK:
                return Move.PAPER
            else:
                return Move.ROCK

    def hardCompMove(self, playerMove):
        """
        Computer makes a move that will make it win all the time
        :param playerMove:
        :return computer move
        """
        if playerMove == Move.ROCK:
            return Move.PAPER
        elif playerMove == Move.PAPER:
            return Move.SCISSORS
        else:
            return Move.ROCK
