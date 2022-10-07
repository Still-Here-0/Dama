from colorama import Style, Back
from ClassState import Mks

class Maker():
    def __init__(self, type:Mks, kill:tuple) -> None:
        self.color = type.value
        self.kill = kill # killed line, killed column

    def getSquare(self) -> Style:
        return self.color + ' ' + Style.RESET_ALL