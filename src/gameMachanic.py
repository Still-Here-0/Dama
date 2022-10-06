from ClassState import TurnState as TS, PlayerTurn as PT, SubState as SS, Windown
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
            return SS.ERROR
    
    line = int(coord[1]) - 1
    column = valid[coord[0]]
    piece = objTable.obj_from_coord(line, column) 
    piece.setSelection()
    objTable.selected_piece = (line, column)
    objTable.setMarkers()

    return SS.NEXT

def moveState(objTable:Table) -> int:
    print('Digite "ESC" para selecionar outra peca')
    moveTo = input('Selecione uma posicao: ')

    if moveTo == 'ESC':
        objTable.backToSelect()
        return SS.BACK

def checkState(objTable:Table) -> int:
    pass

def start_game(objTable:Table) -> Windown:
    p_turn = PT.P1
    turn_state = TS.SELECT
    sub_state = SS.NEXT

    while turn_state != TS.END_GAME:
        objTable.printTable()
        
        if sub_state == SS.ERROR:
            print(Fore.RED + "Valor invalido" + Fore.RESET)
            sub_state = SS.NEXT

        question = "Rodada do "
        question += objTable.p_colors[p_turn.value] + p_turn.name + Fore.RESET
        print(question)

        match turn_state:
            case TS.SELECT:
                sub_state = selectState(objTable, p_turn)
                if sub_state == SS.NEXT:
                    turn_state = TS.MOVE

            case TS.MOVE:
                sub_state = moveState(objTable)
                if sub_state == SS.NEXT:
                    turn_state = TS.CHECK
                
                elif sub_state == SS.BACK:
                    turn_state = TS.SELECT

            case TS.CHECK:
                sub_state = checkState(objTable)

            case TS.PASS:
                p_turn = PT.P1 if p_turn == PT.P2 else PT.P2
        
        if sub_state is None:
            print(f'FULL ERROR!!! {sub_state=}')
            turn_state = TS.END_GAME
    
    return Windown.MENU
