from colorama import Fore, Back, Style
from ClassState import PlayerTurn as PT, Mks

class Piece:
    """
        Da funcionalidade as pecas
    """
    def __init__(self, line:int, column:int, color:Fore, char:str, p_turn:PT) -> None:
        self.line = line
        self.column = column
        self.fore = color           # Cor base
        self.color = color          # Cor atual
        self.char = char
        self.p_turn = p_turn
        self.direct = 1 if p_turn == PT.P1 else -1
        self.selected = False

    def getSquare(self) -> Style:
        return self.color + self.char + Style.RESET_ALL

    def setSelection(self) -> None:
        if not self.selected:
            self.selected = True
            self.color = self.fore + Back.WHITE
        else:
            self.selected = False
            self.color = self.fore

    def getMovPossibilities(self, table_state: list) -> list:       
        movs = self.getNextMov(self.line, self.column)
        attack_mode = len(movs)
        pos_movs = []

        for mov in movs:
            en_line, en_column = mov
            if table_state[en_line][en_column] is None:
                pos_movs.append((en_line, en_column, Mks.MOV, []))
            elif table_state[en_line][en_column].p_turn != self.p_turn:
                pass
        
        return pos_movs

    def getNextMov(self, en_line:int, en_column:int, way:int=0) -> list:
        movs = []
        if way <= 0 and en_column - 1 >= 0:
            movs.append((en_line + self.direct, en_column - 1))
        if way >= 0 and en_column + 1 <= 8:
            movs.append((en_line + self.direct, en_column + 1))
        
        return movs # (line, column)

    def isKillble(self, table_state:list, en_line:int, en_column:int, way) -> bool:
        new_line, new_column = self.getNextMov(en_line, en_column, way)
        return not isinstance(table_state[new_line][new_column], Piece)
