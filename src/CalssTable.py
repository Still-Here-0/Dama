from ClassState import PlayerTurn as PT
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
        self.walls = options[2]                 # defaut: ('[', ']')

        self.selected_piece = None
        self.makers = []

        self.table_state = None #Lista das linhas
        self.setInitPieces()

    def setTableState(self, state) -> None:
        self.table_state = state

    def setMarkers(self):
        piece = self.obj_from_coord(*self.selected_piece)
        mov_list = piece.getMovPossibilities(self.table_state)

        for line, column, type, kill_list in mov_list:
            self.table_state[line][column] = Maker(type, kill_list)
            self.makers.append((line, column))

    def backToSelect(self):
        for line, column in self.makers:
            obj = self.table_state[line][column]
            self.table_state[line][column] = None
        
        piece = self.obj_from_coord(*self.selected_piece)
        piece.setSelection()

    def obj_from_coord(self, line:int, column:int) -> Piece:
        return self.table_state[line][column]

    def printTable(self) -> None:
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
        state = []
        
        for table_line in range(8):
            state_line = []
            for table_column in range(8):
                if table_line <= 2 and table_line%2 == table_column%2:
                    state_line.append(Piece(table_line, table_column, self.p_colors[0], self.char_pieces[0], PT.P1))
                elif table_line >= 5 and table_line%2 == table_column%2:
                    state_line.append(Piece(table_line, table_column, self.p_colors[1], self.char_pieces[1], PT.P2))
                else:
                    state_line.append(None)
            state.append(state_line)
        
        state[3][3] = Piece(table_line, table_column, self.p_colors[1], self.char_pieces[1], PT.P2)
        self.setTableState(state)
