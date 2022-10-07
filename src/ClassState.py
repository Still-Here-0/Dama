from colorama import Back
from enum import Enum

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
    SELECT_ERROR = 6
    MOVE_ERROR = 7