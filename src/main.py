#python -3.10
import gameMachanic as GM
from CalssTable import Table
from colorama import Fore
            

def main():
    opt = [
        (Fore.RED, Fore.YELLOW),
        ('P', 'P'),
        ('[', ']')
    ]
    t = Table(opt)
    GM.start_game(t)

if __name__ == "__main__":
    main()

"""
8 [P][ ][P][ ][P][ ][P][P]
7 [ ][P][ ][P][ ][P][ ][P]
6 [P][ ][P][ ][P][ ][P][ ]
5 [ ][ ][ ][ ][ ][ ][ ][ ]
4 [ ][ ][ ][ ][ ][ ][ ][ ]
3 [ ][P][ ][P][ ][P][ ][P]
2 [P][ ][P][ ][P][ ][P][ ]
1 [ ][P][ ][P][ ][P][ ][P]
   a  b  c  d  e  f  g  h
"""