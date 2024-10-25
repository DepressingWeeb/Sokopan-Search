import sys
import pygame
from collections import deque
from queue import PriorityQueue
from collections import defaultdict
import math
import random

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
GREEN = (0, 127, 0)
BLUE = (0, 0, 200)
RED = (200, 0, 0)
PURPLE = (255, 0, 255)
YELLOW = (255, 255, 51)
AQUA = (127, 255, 212)
CLOCK = pygame.time.Clock()
pygame.init()

from collections import deque


class BFS:
    def __init__(self, board):
        self.board_begin = board
        self.board = board
        self.n_rows = len(board)
        self.n_cols = len(board[0])
        self.walls_coord_set = set()  # Contains coordinates of walls, cannot be changed
        self.target = []  # Contains the switch coordinates sorted, cannot be changed
        for i in range(self.n_rows):
            for j in range(self.n_cols):
                if board[i][j] == '.':
                    self.target.append((i, j))
                elif board[i][j] == '#':
                    self.walls_coord_set.add((i, j))
        self.target.sort()

    def can_push(self, push_dir, char_coord, stones_coord, walls_coord_set):
        # Determine the direction vector based on push_dir
        direction = [(-1, 0), (1, 0), (0, -1), (0, 1)][push_dir]
        char_x, char_y = char_coord
        stone_x, stone_y = char_x + direction[0], char_y + direction[1]
        next_x, next_y = stone_x + direction[0], stone_y + direction[1]

        # Check if the stone's current position is in the stones_coord
        if (stone_x, stone_y) not in stones_coord:
            return False

        # Check if the next position is out of bounds or blocked
        if not (0 <= next_x < self.n_rows and 0 <= next_y < self.n_cols):
            return False
        if (next_x, next_y) in walls_coord_set or (next_x, next_y) in stones_coord:
            return False

        # Valid push
        return True

    def can_move(self, move_dir, char_coord, walls_coord_set):
        direction = [(-1, 0), (1, 0), (0, -1), (0, 1)][move_dir]
        char_x, char_y = char_coord
        next_x, next_y = char_x + direction[0], char_y + direction[1]
        if not (0 <= next_x < self.n_rows and 0 <= next_y < self.n_cols):
            return False
        return (next_x, next_y) not in walls_coord_set

    def is_move_or_push(self, dir, char_coord, stones_coord):
        direction = [(-1, 0), (1, 0), (0, -1), (0, 1)][dir]
        char_x, char_y = char_coord
        next_x, next_y = char_x + direction[0], char_y + direction[1]

        return (next_x, next_y) not in stones_coord

    def BFS(self):
        q = deque()
        visited = set()
        char_coord = (0, 0)
        stones_coord = []
        for i in range(self.n_rows):
            for j in range(self.n_cols):
                if self.board[i][j] == '$':
                    stones_coord.append((i, j))
                elif self.board[i][j] == '@':
                    char_coord = (i, j)

        # Each state: (current char_coord, stone positions, action path)
        q.append((char_coord, stones_coord, ""))

        while q:
            curr_char_coord, curr_stones_coord, path = q.popleft()
            # Check if all stones are on the switches
            if sorted(curr_stones_coord) == self.target:
                return path  # Return the action path
            if (curr_char_coord, tuple(curr_stones_coord)) in visited:
                continue
            visited.add((curr_char_coord, tuple(curr_stones_coord)))
            # Try all 4 possible directions: Up, Down, Left, Right
            for direction in range(4):
                if self.is_move_or_push(direction, curr_char_coord, curr_stones_coord):
                    # Move action
                    if self.can_move(direction, curr_char_coord, self.walls_coord_set):
                        new_char_coord = (curr_char_coord[0] + [-1, 1, 0, 0][direction],
                                          curr_char_coord[1] + [0, 0, -1, 1][direction])
                        q.append((new_char_coord, curr_stones_coord, path + "udlr"[direction]))
                else:
                    #print('Push')
                    # Push action
                    if self.can_push(direction, curr_char_coord, curr_stones_coord, self.walls_coord_set):
                        # Perform the push
                        new_char_coord = (curr_char_coord[0] + [-1, 1, 0, 0][direction],
                                          curr_char_coord[1] + [0, 0, -1, 1][direction])
                        new_stones_coord = list(curr_stones_coord)
                        new_stone_pos = (new_char_coord[0] + [-1, 1, 0, 0][direction],
                                         new_char_coord[1] + [0, 0, -1, 1][direction])
                        new_stones_coord.remove((new_char_coord[0], new_char_coord[1]))
                        new_stones_coord.append(new_stone_pos)
                        q.append((new_char_coord, new_stones_coord, path + "UDLR"[direction]))
                        #visited.add((new_char_coord, tuple(new_stones_coord)))

        return "No solution found"  # If no solution is found


class Visualizer:
    def __init__(self, board):
        self.board_begin = board
        self.board = board
        self.block_size = 64 #constant
        self.n_rows = len(board)
        self.n_cols = len(board[0])
        self.window_width = self.block_size * self.n_cols
        self.window_height = self.block_size * self.n_rows
        self.SCREEN  = pygame.display.set_mode((self.window_width, self.window_height))
        self.rect_coord = [[None for __ in range(self.n_cols)] for _ in range(self.n_rows)]
        for x in range(0, self.window_width, self.block_size):
            for y in range(0, self.window_height, self.block_size):
                rect = pygame.Rect(x, y, self.block_size, self.block_size)
                self.rect_coord[y // self.block_size][x // self.block_size] = rect

        #UI specific
        self.map_tile = pygame.transform.scale(pygame.image.load(r'resources/map/tile001.png').convert_alpha(),
                                               (self.block_size,self.block_size))
        self.stone = pygame.transform.scale(pygame.image.load(r'resources/stone/tile002.png').convert_alpha(),
                                               (self.block_size-25,self.block_size-25))
        self.switch_unactivated = pygame.transform.scale(pygame.image.load(r'resources/switch/tile002.png').convert_alpha(),
                                               (self.block_size-10,self.block_size-10))
        self.tree = pygame.transform.scale(pygame.image.load(r'resources/tree/tile005.png').convert_alpha(),
                                               ((self.block_size-15),self.block_size-15))
        self.character = [pygame.transform.scale(pygame.image.load(f'resources/player/tile00{i}.png').convert_alpha(),
                                               (self.block_size-10,self.block_size-10)) for i in range(4)]
        self.char_direction = 0
        self.frame_rate = 60
        self.current_frame = 0
        for i in range(self.n_rows):
            for j in range(self.n_cols):
                if board[i][j] == '@':
                    self.char_coord = (i,j)


    def render_map(self):
        for i in range(self.n_rows):
            for j in range(self.n_cols):
                x,y,w,h = self.rect_coord[i][j]
                self.SCREEN.blit(self.map_tile,(x,y))
                if board[i][j] == '.':
                    center = self.rect_coord[i][j].center
                    img_rect = self.switch_unactivated.get_rect()
                    img_rect.center = center
                    self.SCREEN.blit(self.switch_unactivated, img_rect)
                elif board[i][j] == '#':
                    center = self.rect_coord[i][j].center
                    img_rect = self.tree.get_rect()
                    img_rect.center = center
                    self.SCREEN.blit(self.tree, img_rect)
                elif board[i][j] == '.$':
                    center = self.rect_coord[i][j].center
                    img_rect_1 = self.switch_unactivated.get_rect()
                    img_rect_1.center = center
                    img_rect_2 = self.stone.get_rect()
                    img_rect_2.center = center
                    self.SCREEN.blit(self.switch_unactivated, img_rect_1)
                    self.SCREEN.blit(self.stone, img_rect_2)

    def render_stone(self):
        for i in range(self.n_rows):
            for j in range(self.n_cols):
                if board[i][j] == '$':
                    center = self.rect_coord[i][j].center
                    img_rect = self.stone.get_rect()
                    img_rect.center = center
                    self.SCREEN.blit(self.stone, img_rect)
    def render_character(self,char_direction):
        for i in range(self.n_rows):
            for j in range(self.n_cols):
                if board[i][j] == '@':
                    center = self.rect_coord[i][j].center
                    img_rect = self.character[char_direction].get_rect()
                    img_rect.center = center
                    self.SCREEN.blit(self.character[char_direction], img_rect)
                elif board[i][j] == '.@':
                    center = self.rect_coord[i][j].center
                    img_rect_1 = self.switch_unactivated.get_rect()
                    img_rect_1.center = center
                    img_rect_2 = self.character[char_direction].get_rect()
                    img_rect_2.center = center
                    self.SCREEN.blit(self.switch_unactivated, img_rect_1)
                    self.SCREEN.blit(self.character[char_direction], img_rect_2)

    def process_command(self,command : str):
        map_dir = {
            'u': (-1, 0,2),
            'd': (1, 0,0),
            'l': (0, -1,3),
            'r': (0, 1,1)
        }
        if command.islower():
            char_x,char_y = self.char_coord
            change_x,change_y,char_direction = map_dir[command]
            board[char_x][char_y]=board[char_x][char_y].replace('@','')
            board[char_x + change_x][char_y + change_y] = (board[char_x + change_x][char_y + change_y]+'@').strip()
            self.char_coord = (char_x+change_x,char_y+change_y)
            self.char_direction = char_direction
        else:
            char_x, char_y = self.char_coord
            change_x, change_y, char_direction = map_dir[command.lower()]
            stone_x, stone_y = char_x + change_x,char_y+ change_y
            stone_x_after_push,stone_y_after_push = char_x + change_x*2,char_y+ change_y*2
            if board[stone_x_after_push][stone_y_after_push] == '.':
                board[stone_x_after_push][stone_y_after_push] = '.$'
            else:
                board[stone_x_after_push][stone_y_after_push] = '$'
            board[stone_x][stone_y] = board[stone_x][stone_y].replace('$','')
            board[stone_x][stone_y] = (board[stone_x][stone_y]+'@').strip()
            board[char_x][char_y]=board[char_x][char_y].replace('@','')
            if board[char_x][char_y]=='':
                board[char_x][char_y] = ' '
            self.char_coord = (char_x + change_x, char_y + change_y)
            self.char_direction = char_direction

    def main_loop(self):
        run = True
        command_str = 'uLulDrrRRRRurD'
        command_lst = [char for char in command_str]
        command_queue = deque(command_lst)
        self.SCREEN.fill(GREEN)
        self.render_map()
        self.render_stone()
        self.render_character(self.char_direction)
        pygame.display.update()
        CLOCK.tick(1)
        while (run):
            self.current_frame+=1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            #only render step once per second
            if len(command_queue)>0 and self.current_frame % self.frame_rate == 0:
                command = command_queue.popleft()
                self.process_command(command)
                self.SCREEN.fill(GREEN)
                self.render_map()
                self.render_stone()
                self.render_character(self.char_direction)
            pygame.display.update()
            CLOCK.tick(self.frame_rate)
        pygame.quit()

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