import pygame
from collections import deque
from timeit import default_timer as timer
from bfs import BFS
from globals import *
class Visualizer:
    def __init__(self, board):
        self.board_begin = board
        self.board = board
        self.block_size = 64 #constant
        self.n_rows = len(self.board)
        self.n_cols = len(self.board[0])
        self.window_width = self.block_size * self.n_cols
        self.window_height = self.block_size * self.n_rows
        self.SCREEN  = pygame.display.set_mode((self.window_width, self.window_height))
        self.rect_coord = [[pygame.Rect(0,0,0,0) for __ in range(self.n_cols)] for _ in range(self.n_rows)]
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
                if self.board[i][j] == '@':
                    self.char_coord = (i,j)


    def render_map(self):
        for i in range(self.n_rows):
            for j in range(self.n_cols):
                x,y,w,h = self.rect_coord[i][j]
                self.SCREEN.blit(self.map_tile,(x,y))
                if self.board[i][j] == '.':
                    center = self.rect_coord[i][j].center
                    img_rect = self.switch_unactivated.get_rect()
                    img_rect.center = center
                    self.SCREEN.blit(self.switch_unactivated, img_rect)
                elif self.board[i][j] == '#':
                    center = self.rect_coord[i][j].center
                    img_rect = self.tree.get_rect()
                    img_rect.center = center
                    self.SCREEN.blit(self.tree, img_rect)
                elif self.board[i][j] == '.$':
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
                if self.board[i][j] == '$':
                    center = self.rect_coord[i][j].center
                    img_rect = self.stone.get_rect()
                    img_rect.center = center
                    self.SCREEN.blit(self.stone, img_rect)
    def render_character(self,char_direction):
        for i in range(self.n_rows):
            for j in range(self.n_cols):
                if self.board[i][j] == '@':
                    center = self.rect_coord[i][j].center
                    img_rect = self.character[char_direction].get_rect()
                    img_rect.center = center
                    self.SCREEN.blit(self.character[char_direction], img_rect)
                elif self.board[i][j] == '.@':
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
            self.board[char_x][char_y]=self.board[char_x][char_y].replace('@','')
            self.board[char_x + change_x][char_y + change_y] = (self.board[char_x + change_x][char_y + change_y]+'@').strip()
            self.char_coord = (char_x+change_x,char_y+change_y)
            self.char_direction = char_direction
        else:
            char_x, char_y = self.char_coord
            change_x, change_y, char_direction = map_dir[command.lower()]
            stone_x, stone_y = char_x + change_x,char_y+ change_y
            stone_x_after_push,stone_y_after_push = char_x + change_x*2,char_y+ change_y*2
            if self.board[stone_x_after_push][stone_y_after_push] == '.':
                self.board[stone_x_after_push][stone_y_after_push] = '.$'
            else:
                self.board[stone_x_after_push][stone_y_after_push] = '$'
            self.board[stone_x][stone_y] = self.board[stone_x][stone_y].replace('$','')
            self.board[stone_x][stone_y] = (self.board[stone_x][stone_y]+'@').strip()
            self.board[char_x][char_y]=self.board[char_x][char_y].replace('@','')
            if self.board[char_x][char_y]=='':
                self.board[char_x][char_y] = ' '
            self.char_coord = (char_x + change_x, char_y + change_y)
            self.char_direction = char_direction

    def main_loop(self):
        run = True
        bfs = BFS(self.board)
        start_time = timer()
        command_str = bfs.BFS()
        end_time = timer()
        actual_time = end_time-start_time
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

#bfs = BFS(self.board)
#print(bfs.BFS())