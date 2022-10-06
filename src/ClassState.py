from colorama import Back
from enum import Enum

class SubState(Enum):
    NEXT = 0
    ERROR = 1
    BACK = 2
    CONTINUE = 3

class Mks(Enum):
    MOV = Back.GREEN
    ATT = Back.RED

class Windown(Enum):
    MENU = 0
    GAME = 1
    MANUAL = 2
    OPTIONS = 3
    QUIT = 4

class PlayerTurn(Enum):
    P1 = 0
    P2 = 1

class TurnState(Enum):
    SELECT = 0
    MOVE = 1
    CHECK = 2
    PASS = 3
    END_GAME = 4