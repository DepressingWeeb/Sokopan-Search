import ctypes
import multiprocessing
import threading
import time
import pygame

from A_star import AStar
from bfs import BFS
from visulizer import  Visualizer
from button import  Button


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

    node_count = multiprocessing.Value('i', 0)
    path_shared = multiprocessing.Array(ctypes.c_char,1000)

    bfs_instance = BFS(grid_2d)
    a_star_instance = AStar(grid_2d,[1,1,1,1,1,1])
    visualizer_instance = Visualizer(grid_2d)

    a_star_process = multiprocessing.Process(target=a_star_instance.A_star, args=(node_count, path_shared))
    #visualizer_thread = threading.Thread(target=visualizer_instance.visualize, args=(node_count, path_shared))

    a_star_process.start()
    visualizer_instance.visualize(node_count,path_shared)
    a_star_process.join()
    #start = time.time()
    #res = AStar(grid_2d,[1,1,1,1,1,1]).A_star()
    #end = time.time()
    #print(res)
    #print(end-start)
    #bfs = BFS(board)
    #print(bfs.BFS())

