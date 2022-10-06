def start_game(objTable) -> None:
    objTable.set_init_pieces()

    players = {1:('vermelhas', Fore.RED), 2:('azuis', Fore.BLUE)}
    turn = 1
    turn_state = 'select' # or 'move'
    valid_selection = True

    while True:
        objTable.print_table()

        question = 'Rodada das '
        question += players[turn][1] + f'{players[turn][0]}!' + Fore.RESET
        print(question)


        match turn_state:
            case 'select':
                valid_selection, selected_obj_pawn = objTable.select_pawn(turn, valid_selection)
                if valid_selection:
                    selected_obj_pawn.is_selected()
                    turn_state = 'move or attack'
            case 'move or attack':
                objTable.set_movements(selected_obj_pawn)
                a = input('')
                if a == '':
                    turn_state = 'check_end_game'
            case 'check_end_game':
                turn_state = 'end_of_turn'
                pass
            case 'end_of_turn':
                turn = 1 if turn == 2 else 2
                turn_state = 'select'

def select_pawn(self, turn:int, valid: bool) -> bool & str:
    question = ''
    if not valid:
        question += Fore.YELLOW + '\nVocê deve selecionar chamando a coluna e depois a linha\n(não selecione um espaço em branco)\nEx: "a1"' + Fore.RESET
    question += '\nQual peça você deseja selecionar? '
    select = input(question).lower()
    
    line, column = self.str_to_coord(select)

    valid = self.is_section_valid(select, line, column, turn)

    obj_pawn = self.obj_pawn_from_coord(line, column)

    return valid, obj_pawn

def get_possible_moves(objTable, obj_table) ->  list and list:
    front = -1 if objTable.team == 2 else 1
    ahead = objTable.coord[0]+front
    right = objTable.coord[1]+1
    left = objTable.coord[1]-1

    normal_movs:list = objTable.normal_moves( ahead, left, right, obj_table.table_state)
    attack_movs:list = objTable.attack_moves([(ahead, left), (ahead, right)], obj_table.table_state)

    return normal_movs, attack_movs

def normal_moves(objTable, ahead, left, right, table_state):
    normal_moves = []
    
    if 0 <= right <= 7:
        if table_state[ahead][right] == None:
            normal_moves.append((ahead, right))
    if 0 <= left <= 7:
        if table_state[ahead][left] == None:
            normal_moves.append((ahead, left))
    
    print(normal_moves)
    return normal_moves

def check_for_enemeis(possible_attack, table_state):
    if 0 <= possible_attack[1] <= 7:
        if table_state[possible_attack[0]][possible_attack[1]] != None:
            return True
    return False

def is_section_valid(objTable, select:str, line:int, column:int, turn:int) -> bool:
        invalid_opts = [
            len(select) != 2, line == -1 or column == -1,
            objTable.table_state[line][column] == None,
            objTable.table_state[line][column].team != turn
        ]

        for invalid_opt in invalid_opts:
            if invalid_opt:
                return False
        
        return True

def str_to_coord(str_coord:str) -> int and int:
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


