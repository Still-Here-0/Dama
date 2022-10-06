from colorama import Style, Back
from ClassState import Mks

class Maker():
    def __init__(self, type:Mks, kill_list:list) -> None:
        self.color = type.value
        self.kill_list = kill_list  # list of coords of enemy pieces

    def getSquare(self) -> Style:
        return self.color + ' ' + Style.RESET_ALL