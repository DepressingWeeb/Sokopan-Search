import ctypes
import multiprocessing
import threading
import time
import pygame

from A_star import AStar
from bfs import BFS
from utils import input_txt_file
from utils import  get_all_output
from visulizer import  Visualizer
from Game import Game

if __name__ == "__main__":
    pygame.init()
    game = Game()
    get_all_output(r'levels')
    game.run()





