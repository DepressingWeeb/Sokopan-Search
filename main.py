import ctypes
import multiprocessing
import threading
import time
import pygame

from A_star import AStar
from bfs import BFS
from visulizer import  Visualizer
from main_screen import MainScreen

if __name__ == "__main__":
    pygame.init()
    #MainScreen().run()
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
    grid_string_3 = '''
############
#  @    .  #
#  ### ### #
#  $       #
#  ### ### #
#          #
############'''
    # Convert the string to a 2D list (grid) of characters
    lines = grid_string_3.splitlines()
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
    board_2 = [
        ['#', '#', '#', '#', '#', '#', '#'],
        ['#', ' ', ' ', '@', ' ', ' ', '#'],
        ['#', ' ', '$', ' ', '$', ' ', '#'],
        ['#', '.', ' ', ' ', ' ', '.', '#'],
        ['#', '#', '#', '#', '#', '#', '#']
    ]
    board_3 = [
        ['#', '#', '#', '#', '#'],
        ['#', ' ', ' ', ' ', '#'],
        ['#', '@', '$', '.', '#'],
        ['#', ' ', '$', '.', '#'],
        ['#', '#', '#', '#', '#']
    ]
    board_4 = [
        ['#', '#', '#', '#', '#'],
        ['#', '@', ' ', '#', '#'],
        ['#', ' ', '.', '$', '#'],
        ['#', '#', '#', '#', '#']
    ]
    visualizer_instance = Visualizer(grid_2d)
    visualizer_instance.visualize()
    #start = time.time()
    #res = AStar(grid_2d,[1,1,1,1,1,1]).A_star()
    #end = time.time()
    #print(res)
    #print(end-start)
    #bfs = BFS(board)
    #print(bfs.BFS())

