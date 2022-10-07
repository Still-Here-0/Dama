from ClassState import TurnState as TS, PlayerTurn as PT, Windown
from ClassMarker import Maker
from CalssTable import Table
from colorama import Fore

def selectState(objTable:Table, turn:PT) -> int:
    valid = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}
    coord = input('Selecione uma peca: ').lower()

    invalids = [
        'len(coord) != 2',
        'not coord[0] in valid.keys()',
        'not coord[1] in [str(x+1) for x in valid.values()]',
        'objTable.table_state[int(coord[1]) - 1][valid[coord[0]]] == None',
        'not objTable.table_state[int(coord[1]) - 1][valid[coord[0]]].p_turn == turn'
    ]
    for isInvalid in invalids:
        if eval(isInvalid):
            return TS.SELECT_ERROR
    
    line = int(coord[1]) - 1
    column = valid[coord[0]]
    objTable.selectPiece(line, column)

    return TS.MOVE

def moveState(objTable:Table) -> int:
    valid = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}
    print('Digite "ESC" para selecionar outra peca')
    moveTo = input('Selecione uma posicao: ')

    if moveTo == 'ESC':
        objTable.unselect()
        return TS.SELECT

    invalids = [
        'len(moveTo) != 2',
        'not moveTo[0] in valid.keys()',
        'not moveTo[1] in [str(x+1) for x in valid.values()]',
        'objTable.table_state[int(moveTo[1]) - 1][valid[moveTo[0]]] == None',
        'not isinstance(objTable.table_state[int(moveTo[1]) - 1][valid[moveTo[0]]], Maker)'
    ]
    for isInvalid in invalids:
        if eval(isInvalid):
            return TS.MOVE_ERROR

    to_line = int(moveTo[1]) - 1
    to_column = valid[moveTo[0]]

    can_kill_again = objTable.movPiece(objTable.table_state, to_line, to_column)

    if can_kill_again:
        objTable.selectPiece(to_line, to_column)
        return TS.MOVE

    return TS.CHECK

def checkState(objTable:Table) -> int:
    return TS.PASS

def start_game(objTable:Table) -> Windown:
    p_turn = PT.P1
    turn_state = TS.SELECT
    error_msg = ''

    while turn_state != TS.END_GAME:
        objTable.printTable()

        if error_msg:
            print(Fore.RED + error_msg + Fore.RESET)
            error_msg = ''

        round = "Rodada do "
        round += objTable.p_colors[p_turn.value] + p_turn.name + Fore.RESET
        print(round)

        match turn_state:
            case TS.SELECT:
                turn_state = selectState(objTable, p_turn)
                if turn_state == TS.SELECT_ERROR:
                    error_msg = 'Falha ao selecionar, tente novamente!'
                    turn_state = TS.SELECT

            case TS.MOVE:
                turn_state = moveState(objTable)
                if turn_state == TS.MOVE_ERROR:
                    error_msg = 'Falha ao mover, tente novamente!'
                    turn_state = TS.MOVE

            case TS.CHECK:
                turn_state = checkState(objTable)

            case TS.PASS:
                p_turn = PT.P1 if p_turn == PT.P2 else PT.P2
                turn_state = TS.SELECT
        
        if turn_state is None:
            print(f'FULL ERROR!!! {turn_state   =}')
            turn_state = TS.END_GAME
    
    return Windown.MENU
