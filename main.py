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


    board_inp,weight_list_inp = input_txt_file(r'levels/Level_3.txt')
    '''
    time_taken = multiprocessing.Value('d',0)
    node = multiprocessing.Value('i',0)
    path = multiprocessing.Array(ctypes.c_char, 10000)
    stop_signal = multiprocessing.Event()
    a_star_instance = AStar(board_file,weight_list=[34,2,43,12,3])
    res = a_star_instance.A_star(time_taken,node,path,stop_signal)
    print(res)
    '''
    visualizer_instance = Visualizer(board_inp,weight_list_inp)
    visualizer_instance.visualize()


