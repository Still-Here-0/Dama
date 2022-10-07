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

    def moved(self, to_line, to_column):
        self.line = to_line
        self.column = to_column

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
        movs = self.getFrontMov(self.line, self.column)
        killble = []
        normal_movs = []
        for en_line, en_column in movs:
            if table_state[en_line][en_column] is None:
                normal_movs.append((en_line, en_column, Mks.MOV, ()))
            elif table_state[en_line][en_column].p_turn != self.p_turn:
                kill = self.setKillble(table_state, en_line, en_column, self.getFrontMov)
                if kill:
                    killble.append(kill)
        
        killble.extend(self.checkKillbleBack(table_state))

        if killble:
            return killble
        else:
            return normal_movs

    def getKillbleMovs(self, table_state:list):
        movs = self.getFrontMov(self.line, self.column)
        killble = []
        for en_line, en_column in movs:
            if table_state[en_line][en_column] is None:
                continue
            elif table_state[en_line][en_column].p_turn != self.p_turn:
                kill = self.setKillble(table_state, en_line, en_column, self.getFrontMov)
                if kill:
                    killble.append(kill)
        
        killble.extend(self.checkKillbleBack(table_state))

        return killble

    def checkKillbleBack(self, table_state):
        back_movs = self.getBackMov(self.line, self.column)
        killble = []
        for en_line, en_column in back_movs:
            if table_state[en_line][en_column] is None:
                continue
            elif table_state[en_line][en_column].p_turn != self.p_turn:
                kill = self.setKillble(table_state, en_line, en_column, self.getBackMov)
                if kill:
                    killble.append(kill)
        
        return killble

    def setKillble(self, table_state, en_line, en_column, getMov):
        way = en_column - self.column
        if self.isKillble(table_state, en_line, en_column, way):
            new_line, new_column = getMov(en_line, en_column, way)[0]
            return (new_line, new_column, Mks.ATT, (en_line, en_column))
        return []

    def getBackMov(self, en_line:int, en_column:int, way:int=0) -> list:
        movs = []
        if way <= 0 and en_column - 1 >= 0:
            movs.append((en_line - self.direct, en_column - 1))
        if way >= 0 and en_column + 1 <= 8:
            movs.append((en_line - self.direct, en_column + 1))

        return movs # [(line, column)...]

    def getFrontMov(self, en_line:int, en_column:int, way:int=0) -> list:
        movs = []
        if way <= 0 and en_column - 1 >= 0:
            movs.append((en_line + self.direct, en_column - 1))
        if way >= 0 and en_column + 1 <= 8:
            movs.append((en_line + self.direct, en_column + 1))
        
        return movs # [(line, column)...]

    def isKillble(self, table_state:list, en_line:int, en_column:int, way:int) -> bool:
        new_line, new_column = self.getFrontMov(en_line, en_column, way)[0]
        return not isinstance(table_state[new_line][new_column], Piece)

    def __del__(self):
        cood = (self.line, self.column)
        input(f'I was deleted {cood}')