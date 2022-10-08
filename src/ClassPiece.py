from colorama import Fore, Back, Style
from ClassState import PlayerTurn as PT, Mks

class Piece:
    """
        Da funcionalidade as pecas
    """
    def __init__(self, line:int, column:int, color:Fore, char:str, p_turn:PT) -> None:
        self.line = line
        self.column = column
        self.coord = (line, column)
        self.fore = color           # Cor base
        self.color = color          # Cor atual
        self.char = char
        self.p_turn = p_turn
        self.direct = 1 if p_turn == PT.P1 else -1
        self.selected = False

    def moved(self, to_line:int, to_column:int) -> None:
        """redefine a linha q coluna do peca

        Args:
            to_line (int): linha que a peca esta
            to_column (int): coluna que a peca esta
        """
        self.line = to_line
        self.column = to_column
        self.coord = (to_line, to_column)

    def getSquare(self) -> Style:
        """Pega o sprite da peca

        Returns:
            Style: retorna o sprite da peca
        """
        return self.color + self.char + Style.RESET_ALL

    def setSelection(self) -> None:
        """Troca o backgroud do sprite, selecionando a peca
        """
        if not self.selected:
            self.selected = True
            self.color = self.fore + Back.WHITE
        else:
            self.selected = False
            self.color = self.fore

    def getMovPossibilities(self, table_state: list) -> list:
        """Define as casa que a peca pode ser movida. Caso haja a possibilidade de comer pecas os movimentos normais nao seram contados.

        Args:
            table_state (list): o atual estado do tabuleiro

        Returns:
            list: lista de tuplas com as coordenadas possiveis para movimentacao [(linha, coluna), ...]
        """
        front_movs = self.getFrontMov(self.line, self.column)
        killble = []
        normal_movs = []
        
        # Na frente podemos comer pecas ou andar
        for en_line, en_column in front_movs:
            if table_state[en_line][en_column] is None:
                normal_movs.append((en_line, en_column, Mks.MOV, ()))
            elif table_state[en_line][en_column].p_turn != self.p_turn:
                killble.extend(self.setIfKillble(table_state, en_line, en_column))

        # Nas costas, so podemos comer pecas
        back_movs = self.getBackMov(self.line, self.column)
        for en_line, en_column in back_movs:
            if table_state[en_line][en_column] is None:
                pass
            elif table_state[en_line][en_column].p_turn != self.p_turn:
                killble.extend(self.setIfKillble(table_state, en_line, en_column))

        if killble:
            return killble
        else:
            return normal_movs

    def getKillbleMovs(self, table_state:list) -> list:
        """Procura casas que a peca possa ser movida para comer outras pecas.

        Args:
            table_state (list): o atual estado do tabuleiro

        Returns:
            list: retorna uma lista de tuplas [(linha, coluna), ...], ou uma lista vazia
        """
        movs = self.getFrontMov(self.line, self.column)
        movs.extend(self.getBackMov(self.line, self.column))
        killble = []
        for en_line, en_column in movs:
            if table_state[en_line][en_column] is None:
                pass
            elif table_state[en_line][en_column].p_turn != self.p_turn:
                killble.extend(self.setIfKillble(table_state, en_line, en_column))

        return killble

    def canKill(self, table_state:list) -> bool:
        """Checa se uma peca pode comer outra

        Args:
            table_state (list): estado do tabuleiro atual

        Returns:
            bool: True -> pode moder | False -> n pode comer
        """
        killble_pieces = self.getKillbleMovs(table_state)
        
        if killble_pieces: # se n estiver vazio
            return True
        return False

    def setIfKillble(self, table_state:list, en_line:int, en_column:int) -> list: #
        """checa se uma peca pode ser morta pela peca atual (self.)

        Args:
            table_state (list): estado atual do tabuleiro
            en_line (int): linha da peca inimiga
            en_column (int): coluna da peca inimiga

        Returns:
            list: _description_
        """
        d_column, movFunc = self.getDAndMovFunc(en_line, en_column)

        if self.isKillble(table_state, en_line, en_column):
            mov = movFunc(en_line, en_column, d_column)
            return [(new_line, new_column, Mks.ATT, (en_line, en_column)) for new_line, new_column in mov]
        
        return []

    def getFrontMov(self, en_line:int, en_column:int, way:int=0) -> list:
        """Pega os movimentos que a peca pode fazer para frente

        Args:
            en_line (int): linha da peca inimiga
            en_column (int): coluna da peca inimiga
            way (int, optional): 1 -> vai para direita, -1 -> vai para esquerda, 0 -> vai para os dois lados. Defaults to 0.

        Returns:
            list: lista de tuplas com as coordenadas possiveis para movimentacao [(linha, coluna), ...]
        """
        movs = []
        next_line = en_line + self.direct

        if next_line > 7 or next_line < 0:
            return movs

        if way <= 0 and en_column - 1 >= 0:
            movs.append((next_line, en_column - 1))
        if way >= 0 and en_column + 1 <= 7:
            movs.append((next_line, en_column + 1))
        
        return movs # [(line, column)...]

    def getBackMov(self, en_line:int, en_column:int, way:int=0) -> list:
        """Pega os movimentos que a peca pode fazer para as costas

        Args:
            en_line (int): linha da peca inimiga
            en_column (int): coluna da peca inimiga
            way (int, optional): 1 -> vai para direita, -1 -> vai para esquerda, 0 -> vai para os dois lados. Defaults to 0.

        Returns:
            list: lista de tuplas com as coordenadas possiveis para movimentacao [(linha, coluna), ...]
        """
        movs = []
        next_line = en_line - self.direct

        if next_line > 7 or next_line < 0:
            return movs

        if way <= 0 and en_column - 1 >= 0:
            movs.append((en_line - self.direct, en_column - 1))
        if way >= 0 and en_column + 1 <= 7:
            movs.append((en_line - self.direct, en_column + 1))

        return movs

    def isKillble(self, table_state:list, en_line:int, en_column:int) -> bool:
        """Indica se um peca pode ser morta pela peca atual (self.)

        Args:
            table_state (list): estado atual do tabuleiro
            en_line (int): linha da peca inimiga
            en_column (int): coluna da peca inimiga

        Returns:
            bool: True -> peca pode ser morta; False -> peca nao pode ser morta
        """
        d_column, movFunc = self.getDAndMovFunc(en_line, en_column)
        mov = movFunc(en_line, en_column, d_column)
        
        if len(mov) > 1:
            raise Exception(f"Erro ao definir mov em Piece/isKillble {mov=}")

        for new_line, new_column in mov:
            if not isinstance(table_state[new_line][new_column], Piece):
                return True

        return False

    def getDAndMovFunc(self, en_line:int, en_column:int) -> tuple:
        """Determina se a peca esta indo para direita ou para esquerda e qual funcao de movimento usar

        Args:
            en_line (int): linha da peca inimiga
            en_column (int): coluna da peca inimiga

        Returns:
            tuple: [0] -> 1:direita | -1: esquerda || [1] -> funcao a ser utilizada
        """
        d_line = (en_line - self.line)*self.direct        # 1 -> frente | -1 -> costas
        d_column = en_column - self.column  # 1 -> direita| -1 -> esquerda
        func = {1:self.getFrontMov, -1:self.getBackMov}

        return d_column, func[d_line]

    # def __del__(self):
    #     cood = (self.line, self.column)
    #     input(f'I was deleted {cood}')
