#python -3.10
from colorama import Fore, Back, Style
import os

class Piece:
    def __init__(self, line:int, column:int, color:Fore) -> None:
        teams = {Fore.RED:1, Fore.BLUE:2}
        self.coord = (line, column)
        self.fore = color
        self.color = color
        self.team = teams[color]

    def is_selected(self, selected=True):
        if selected:
            self.color = self.fore + Back.WHITE
        else:
            self.color = self.fore

    def move(self):
        pass

    def get_possible_moves(self, obj_table) ->  list and list:
        front = -1 if self.team == 2 else 1
        ahead = self.coord[0]+front
        right = self.coord[1]+1
        left = self.coord[1]-1

        normal_movs:list = self.normal_moves( ahead, left, right, obj_table.table_state)
        attack_movs:list = self.attack_moves([(ahead, left), (ahead, right)], obj_table.table_state)

        return normal_movs, attack_movs 

    def normal_moves(self, ahead, left, right, table_state):
        normal_moves = []
        
        if 0 <= right <= 7:
            if table_state[ahead][right] == None:
                normal_moves.append((ahead, right))
        if 0 <= left <= 7:
            if table_state[ahead][left] == None:
                normal_moves.append((ahead, left))
        
        print(normal_moves)
        return normal_moves

    def attack_moves(self, possible_attacks, table_state):
        return
        attack_moves = []

        while True:
            possible_attack = possible_attacks.pop(0)
            check_way = self.check_for_enemeis(possible_attack, table_state)
            
            if check_way:
                check_atk_way = self.check_attack(possible_attack, table_state)
                if check_atk_way:
                    attack_moves.append('')

            if len(possible_attacks) == 0:
                break

    def check_for_enemeis(self, possible_attack, table_state):
        if 0 <= possible_attack[1] <= 7:
            if table_state[possible_attack[0]][possible_attack[1]] != None:
                return True
        return False

    def check_attack(self, possible_attack, table_state):
        pass

    def attack(self, attacked):
        pass

class Table:
    def __init__(self, start:bool=True) -> None:
        self.table_state = None #Lista das linhas (que são listas das posições)
        
        if start:
            self.start_game()
    
    def start_game(self) -> None:
        self.set_init_pieces()

        players = {1:('vermelhas', Fore.RED), 2:('azuis', Fore.BLUE)}
        turn = 1
        turn_state = 'select' # or 'move'
        valid_selection = True

        while True:
            self.print_table()

            question = 'Rodada das '
            question += players[turn][1] + f'{players[turn][0]}!' + Fore.RESET
            print(question)


            match turn_state:
                case 'select':
                    valid_selection, selected_obj_pawn = self.select_pawn(turn, valid_selection)
                    if valid_selection:
                        selected_obj_pawn.is_selected()
                        turn_state = 'move'
                case 'move':
                    self.set_movements(selected_obj_pawn)
                    a = input('')
                    if a == '':
                        turn_state = 'check_end_game'
                case 'check_end_game':
                    turn_state = 'end_of_turn'
                    pass
                case 'end_of_turn':
                    turn = 1 if turn == 2 else 2
                    turn_state = 'select'

    def set_movements(self, obj_pawn:Piece):
        list_of_moves = obj_pawn.get_possible_moves(self)

    def select_pawn(self, turn:int, valid: bool) -> bool and str:
        question = ''
        if not valid:
            question += Fore.YELLOW + '\nVocê deve selecionar chamando a coluna e depois a linha\n(não selecione um espaço em branco)\nEx: "a1"' + Fore.RESET
        question += '\nQual peça você deseja selecionar? '
        select = input(question).lower()
        
        line, column = self.str_to_coord(select)

        valid = self.is_section_valid(select, line, column, turn)

        obj_pawn = self.obj_pawn_from_coord(line, column)

        return valid, obj_pawn

    def obj_pawn_from_coord(self, line:int, column:int) -> Piece:
        return self.table_state[line][column]

    def is_section_valid(self, select:str, line:int, column:int, turn:int) -> bool:
        try:
            if len(select) != 2:
                raise ValueError

            if line == -1 or column == -1:
                raise ValueError

            if self.table_state[line][column] == None:
                raise ValueError
            
            if self.table_state[line][column].team != turn:
                raise ValueError
        
        except ValueError:
            return False
        else:
            return True

    def str_to_coord(self, str_coord:str) -> int and int:
        change = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7}
        try:
            line = int(str_coord[1]) - 1
            column = change[str_coord[0]]

            if not(0 <= line <= 7): #As linhas vão de 1 à 8, como line = linha - 1
                raise ValueError

        except (KeyError, ValueError, IndexError):
            return -1, -1
        else:
            return line, column

    def clear_terminal(self) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_table(self) -> None:
        self.clear_terminal()
        for index0 in range(7, -1, -1):
            line = ''
            line += f'{index0 + 1} '
            for index1, square in enumerate(self.table_state[index0]):
                if square != None:
                    pwan = square.color + 'P' + Style.RESET_ALL
                    line += f'[{pwan}]'
                else:
                    line += '[ ]'
            print(line)
        print('   a  b  c  d  e  f  g  h')

    def set_init_pieces(self) -> tuple:
        state = []
        
        for table_line in range(8):
            state_line = []
            for squares in range(8):
                if table_line <= 1:
                    state_line.append(Piece(table_line, squares, Fore.RED))
                elif table_line >= 6:
                    state_line.append(Piece(table_line, squares, Fore.BLUE))
                else:
                    state_line.append(None)
            state.append(state_line)
        
        self.table_state = state

    def teste(self):
        self.set_init_pieces()
        for line in self.table_state:
            for square in line:
                if square != None:
                    print(square.team)
                else:
                    print(square)
            print('--------')

if __name__ == "__main__":
    mesa = Table()

"""
1 [P][P][P][P][P][P][P][P]
2 [P][P][P][P][P][P][P][P]
3 [ ][ ][ ][ ][ ][ ][ ][ ]
4 [ ][ ][ ][ ][ ][ ][ ][ ]
5 [ ][ ][ ][ ][ ][ ][ ][ ]
6 [ ][ ][ ][ ][ ][ ][ ][ ]
7 [P][P][P][P][P][P][P][P]
8 [P][P][P][P][P][P][P][P]
   a  b  c  d  e  f  g  h
"""