import time

import pygame

from A_star import AStar
from bfs import BFS
from visulizer import  Visualizer


if __name__ == "__main__":
    pygame.init()
    grid_string = '''
#######  
  #     #
  # .$. #
 ## $@$ #
 #  .$. #
 #      #
 ########'''
    grid_string_2 = '''
    #####          
    #   #          
    #$  #          
  ###  $##         
  #  $ $ #         
### # ## #   ######
#   # ## #####  ..#
# $  $          ..#
##### ### #@##  ..#
    #     #########
    #######        '''
    # Convert the string to a 2D list (grid) of characters
    lines = grid_string.splitlines()
    lines.pop(0)
    grid_2d = [list(line) for line in lines]
    print(grid_2d)
    board = [
        ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
        ['#', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
        ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
        ['#', ' ', '$', ' ', '$', ' ', ' ', ' ', ' ', ' ', '#'],
        ['#', '.', ' ', '@', ' ', ' ', ' ', ' ', '.', ' ', '#'],
        ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#']
    ]
    visualizer = Visualizer(board=grid_2d)
    visualizer.main_loop()
    #start = time.time()
    #res = AStar(grid_2d,[1,1,1,1,1,1]).A_star()
    #end = time.time()
    #print(res)
    #print(end-start)
    #bfs = BFS(board)
    #print(bfs.BFS())