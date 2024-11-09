import os.path
import pygame
import argparse
from utils import  get_all_output
from Game import Game
from utils import to_output
if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='Sokoban-Solver',
                                     description='Solve weighted sokoban puzzle',
                                     formatter_class=argparse.HelpFormatter)
    parser.add_argument('-m', '--mode', default='gui', type=str,
                        choices=['cli','gui'],
                        help='Run the script in \'cli\' mode or \'gui\' mode')
    parser.add_argument('-p', '--path', default=None, type=str, nargs='+',
                        help='Path to a level(txt) file if using cli mode')
    args = parser.parse_args()
    if args.mode == 'gui':
        pygame.init()
        game = Game()
        game.run()
    else:
        if args.path is None:
            print('No input specified, perform the solve on all of the levels in levels/ by default')
            get_all_output(r'levels')
        else:
            file_path = args.path[0]
            filename, file_extension = os.path.splitext(file_path)
            if os.path.isfile(file_path) and file_extension =='.txt':
                to_output(args.path[0])
                print('Done')
            else:
                raise ValueError('Something is wrong with file path input')






