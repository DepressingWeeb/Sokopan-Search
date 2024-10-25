import pygame
from bfs import BFS
from visulizer import  Visualizer


if __name__ == "__main__":
    pygame.init()
    board = [
        ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
        ['#', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
        ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
        ['#', ' ', '$', ' ', '$', ' ', ' ', ' ', ' ', ' ', '#'],
        ['#', '.', ' ', '@', ' ', ' ', ' ', ' ', '.', ' ', '#'],
        ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#']
    ]

    visualizer = Visualizer(board=board)
    visualizer.main_loop()
    #bfs = BFS(board)
    #print(bfs.BFS())