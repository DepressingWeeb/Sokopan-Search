import ctypes
import multiprocessing
import threading
import time
import pygame

from A_star import AStar
from bfs import BFS
from utils import input_txt_file
from visulizer import  Visualizer
from main_screen import MainScreen
import sys

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
    grid_string_4='''
#####    
#   #####
# # #   #
# $   $ #
#..#$#$##
#.@$   # 
#..  ### 
######   '''
    # Convert the string to a 2D list (grid) of characters
    lines = grid_string_4.splitlines()
    lines.pop(0)
    grid_2d = [list(line) for line in lines]
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
    weight_list = [1,3]
    board_4 = [
        ['#', '#', '#', '#', '#'],
        ['#', '@', ' ', '#', '#'],
        ['#', ' ', '.', '$', '#'],
        ['#', '#', '#', '#', '#']
    ]
    board_5 = [
        ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
        ['#', ' ', ' ', ' ', ' ', ' ', '@', ' ', ' ', ' ', '#'],
        ['#', '.', ' ', ' ', ' ', '$', '$', ' ', ' ', ' ', '#'],
        ['#', ' ', ' ', ' ', ' ', ' ', '.', ' ', ' ', ' ', '#'],
        ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#']
    ]

    board_inp,weight_list_inp = input_txt_file(r'levels/Text10.txt')

    visualizer_instance = Visualizer(grid_2d,[34,2,43,12,3])
    visualizer_instance.visualize()
    time_taken = multiprocessing.Value('d',0)
    node = multiprocessing.Value('i',0)
    path = multiprocessing.Array(ctypes.c_char, 10000)
    stop_signal = multiprocessing.Event()
    a_star_instance = AStar(board_inp,weight_list=[1,1,1,1,1,1])
    #res = a_star_instance.A_star(time_taken,node,path,stop_signal)
    a_star_instance.preprocess()



