from ClassState import PlayerTurn as PT, Mks
from ClassMarker import Maker
from ClassPiece import Piece
import general as gen

class Table:
    """
    Display do tabuleiro
    
    Singleton
    """
    def __init__(self, options:list) -> None:
        self.p_colors:tuple = options[0]        # defaut: (Fore.BLUE, Fore.YELLOW)
        self.char_pieces:tuple = options[1]     # defaut: ('P', 'P')
        self.walls:tuple = options[2]           # defaut: ('[', ']')

        self.last_selected_piece:Piece = None
        self.makers:list = []

        self.table_state = None #Lista das linhas
        self.setInitPieces()

    def checkForEndGame(self, turn:PT) -> bool:
        """Checa se o jogo acabou

        Args:
            turn (PT): turno do jogador

        Returns:
            bool: True -> acabou | False -> nao acabou
        """
        moveble_pieces = 0
        for line in self.table_state:
            for square in line:
                if not isinstance(square, Piece):
                    continue
                
                if not square.getMovPossibilities(self.table_state):
                    continue
                    
                if square.p_turn != turn:
                    moveble_pieces += 1

        if moveble_pieces == 0:
            return True
        
        return False

    def setTableState(self, state:list) -> None:
        """define o estado do tabuleiro (evite usar esse motodo)

        Args:
            state (list): estado do tabuleiro
        """
        self.table_state = state

    def setMarkers(self) -> None:
        """Coloca os objs markers no tabuleiro
        """
        mov_list = self.last_selected_piece.getMovPossibilities(self.table_state)

        for line, column, type, kill in mov_list:
            self.table_state[line][column] = Maker(type, kill)
            self.makers.append((line, column))

    def movPiece(self, to_line:int, to_column:int) -> bool:
        """move a peca selecionada e deleta as pecas que ela comeu

        Args:
            to_line (int): linha que a peca selecionada ira se mover
            to_column (int): coluna que a peca selecionada ira se mover
        Returns:
            bool: True -> comeu uma peca | False -> nao comeu uma peca
        """
        killed = False
        if self.table_state[to_line][to_column].kill:
            en_line, en_column = self.table_state[to_line][to_column].kill
            self.table_state[en_line][en_column] = None
            killed = True

        self.unselect()
        self.table_state[self.last_selected_piece.line][self.last_selected_piece.column] = None
        self.table_state[to_line][to_column] = self.last_selected_piece
        self.last_selected_piece.moved(to_line, to_column)
        return killed

    def isKilling(self, turn:PT) -> bool:
        """Checa se e possivel comer uma peca

        Args:
            turn (PT): turno do jogador

        Returns:
            bool: True -> e possivel comer uma peca | False -> n e possivel comer uma peca
        """
        for line in self.table_state:
            for square in line:
                if not isinstance(square, Piece):
                    continue
                    
                if square.p_turn != turn:
                    continue
                
                if square.canKill(self.table_state):
                    return True
        
        return False

    def selectPiece(self, line:int, column:int, must_kill:bool=False) -> bool:
        """Seleciona a peca indicada pela coordenada e posiciona os marcadores

        Args:
            line (int): linha da peca
            column (int): coluna da peca

        Returns:
            bool: True -> has selected; 
        """
        piece = self.objFromCoord(line, column)

        if must_kill and not piece.canKill(self.table_state):
            return False # N pode selecionar

        piece.setSelection()
        self.last_selected_piece = piece
        self.setMarkers()

        return True

    def unselect(self):
        """Retira os markers e desseleciona o obj peca posteriormente selecionado
        """
        for line, column in self.makers:
            self.table_state[line][column] = None
        
        self.makers = []
        self.last_selected_piece.setSelection()

    def objFromCoord(self, line:int, column:int) -> Piece:
        """Pega uma peca que esta dentro do tabuleiro de acordo com seu posicionamento

        Args:
            line (int): linha da peca
            column (int): coluna da peca

        Returns:
            Piece: obj peca que esta nas coordenadas indicadas
        """
        return self.table_state[line][column]

    def printTable(self) -> None:
        """Apaga todo no terminal e printa linha por linha do tabuleiro na tela, da 8 a 1.
        """
        gen.clear_terminal()
        for line_index in range(7, -1, -1):
            printable_line = f'{line_index + 1} '
            for square in self.table_state[line_index]:
                if square != None: # eh um piao
                    printable_line += f'{self.walls[0]}{square.getSquare()}{self.walls[1]}'
                else: # espaco vazio
                    printable_line += f'{self.walls[0]} {self.walls[1]}'
            print(printable_line)
        print('   a  b  c  d  e  f  g  h')

    def setInitPieces(self) -> None:
        """Coloca as pecas nas posicoes iniciais de um jogo de damas
        """
        state = []
        
        for table_line in range(8):
            state_line = []
            for table_column in range(8):
                if table_line <= 2 and table_line%2 == table_column%2:
                    # state_line.append(None)
                    state_line.append(Piece(table_line, table_column, self.p_colors[0], self.char_pieces[0], PT.P1))
                elif table_line >= 5 and table_line%2 == table_column%2:
                    # state_line.append(None)
                    state_line.append(Piece(table_line, table_column, self.p_colors[1], self.char_pieces[1], PT.P2))
                else:
                    state_line.append(None)
            state.append(state_line)
        # state[5][5] = Piece(5, 5, self.p_colors[0], self.char_pieces[0], PT.P1)
        # state[1][1] = Piece(1, 1, self.p_colors[1], self.char_pieces[1], PT.P2)
        self.setTableState(state)
