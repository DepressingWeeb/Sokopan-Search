import ctypes
import multiprocessing

import pygame
from collections import deque
from timeit import default_timer as timer
from copy import  deepcopy

from A_star import AStar
from UCS import UCS
from bfs import BFS
from dfs import DFS
from globals import *
class Visualizer:
    def __init__(self, board, weight_list=None):
        if weight_list is None:
            weight_list = [0, 0, 0, 0, 0, 0, 0]
        self.board_begin = board
        self.board = board
        self.weight_list = weight_list
        self.n_rows = len(self.board)
        self.n_cols = len(self.board[0])
        self.block_size = 640//self.n_rows
        self.window_width = self.block_size * self.n_cols
        self.window_height = self.block_size * self.n_rows
        self.panel_width = 200
        self.panel_rect = (0,0,self.panel_width,self.window_height)
        self.SCREEN = pygame.display.set_mode((self.window_width + self.panel_width, self.window_height))
        self.rect_coord = [[pygame.Rect(0,0,0,0) for __ in range(self.n_cols)] for _ in range(self.n_rows)]
        for x in range(0, self.window_width, self.block_size):
            for y in range(0, self.window_height, self.block_size):
                rect = pygame.Rect(self.panel_width+x, y, self.block_size, self.block_size)
                self.rect_coord[y // self.block_size][x // self.block_size] = rect

        self.char_direction = 0

        self.frame_rate = 60
        self.current_frame = 0

        self.algorithm_buttons = ["BFS", "DFS", "UCS", "A*"]

        # Load and scale images
        self.load_images()

        # Button positions (based on dynamic height)
        self.button_height = int(self.window_height * 0.1)  # Adjust as needed
        self.button_positions = [
            (self.panel_width * 0.1, self.window_height * (0.1 + i * 0.12))
            for i in range(len(self.algorithm_buttons))
        ]

        # Ribbon and stats position
        self.ribbon_position = (self.panel_width * 0.1, self.window_height * 0.66)
        self.banner_position = (self.panel_width * 0.05, self.window_height * 0.69)

        for i in range(self.n_rows):
            for j in range(self.n_cols):
                if self.board[i][j] == '@':
                    self.char_coord = (i,j)

        # Control variables
        self.current_process = None
        self.stop_signal = multiprocessing.Event()  # Signal to stop running algorithms
        self.selected_algorithm = None
        self.node_count = multiprocessing.Value('i', 0)
        self.path_shared = multiprocessing.Array(ctypes.c_char, 1500)
        self.time_taken = multiprocessing.Value('d', 0)
        #self.step = 0
        self.weight_pushed = 0
        self.board_states = []
        self.current_state_index = -1

        self.pause = False
        self.flag_no_sol_found = False
        self.flag_pass = False

    def load_images(self):
        # UI specific
        self.map_tile = pygame.transform.scale(pygame.image.load(r'resources/map/tile001.png').convert_alpha(),
                                               (self.block_size, self.block_size))
        self.stone = pygame.transform.scale(pygame.image.load(r'resources/stone/tile004.png').convert_alpha(),
                                            (self.block_size - 25, self.block_size - 25))
        self.switch_unactivated = pygame.transform.scale(
            pygame.image.load(r'resources/switch/tile005.png').convert_alpha(),
            (self.block_size - 10, self.block_size - 10))
        self.tree = pygame.transform.scale(pygame.image.load(r'resources/tree/tile005.png').convert_alpha(),
                                           ((self.block_size - 15), self.block_size - 15))
        self.character = [pygame.transform.scale(pygame.image.load(f'resources/player/tile00{i}.png').convert_alpha(),
                                                 (self.block_size - 10, self.block_size - 10)) for i in range(4)]
        self.panel_bg = pygame.image.load("resources/background/panel_bg.jpg")
        # Load button images with hover effect
        self.button_img = pygame.image.load("resources/ui/Button_3Slides.png")
        self.button_pressed_img = pygame.image.load("resources/ui/Button_3Slides_Pressed.png")
        self.button_img = pygame.transform.scale(self.button_img, (self.panel_width * 0.8, int(self.window_height * 0.1)))
        self.button_pressed_img = pygame.transform.scale(self.button_pressed_img,
                                                         (self.panel_width * 0.8, int(self.window_height * 0.1)))

        # Load ribbon and banner for stats section
        self.ribbon_img = pygame.image.load("resources/ui/Ribbon.png")
        self.ribbon_img = pygame.transform.scale(self.ribbon_img, (self.panel_width * 0.8, int(self.window_height * 0.075)))
        self.result_ribbon = pygame.transform.scale(self.ribbon_img, (250,125))
        self.banner_img = pygame.image.load("resources/ui/banner.png")
        self.banner_img = pygame.transform.scale(self.banner_img, (self.panel_width * 0.9, int(self.window_height * 0.3)))

        # Load other control buttons
        self.back_button_img = pygame.image.load("resources/ui/Back_Button.png")
        self.pause_button_img = pygame.image.load("resources/ui/Pause_Button.png")
        self.reset_button_img = pygame.image.load("resources/ui/Reset_Button.png")
        self.back_button_img = pygame.transform.scale(self.back_button_img,
                                                      (int(self.panel_width * 0.25), int(self.panel_width * 0.25)))
        self.pause_button_img = pygame.transform.scale(self.pause_button_img,
                                                       (int(self.panel_width * 0.25), int(self.panel_width * 0.25)))
        self.reset_button_img = pygame.transform.scale(self.reset_button_img,
                                                       (int(self.panel_width * 0.25), int(self.panel_width * 0.25)))
        self.back_button_pressed_img = pygame.image.load("resources/ui/Back_Button_Pressed.png")
        self.pause_button_pressed_img = pygame.image.load("resources/ui/Pause_Button_Pressed.png")
        self.reset_button_pressed_img = pygame.image.load("resources/ui/Reset_Button_Pressed.png")
        self.back_button_pressed_img = pygame.transform.scale(self.back_button_pressed_img,
                                                              (int(self.panel_width * 0.25),
                                                               int(self.panel_width * 0.25)))
        self.pause_button_pressed_img = pygame.transform.scale(self.pause_button_pressed_img,
                                                               (int(self.panel_width * 0.25),
                                                                int(self.panel_width * 0.25)))
        self.reset_button_pressed_img = pygame.transform.scale(self.reset_button_pressed_img,
                                                               (int(self.panel_width * 0.25),
                                                                int(self.panel_width * 0.25)))

    def render_text(self, text, font, color, pos):
        text_surface = font.render(text, True, color)
        self.SCREEN.blit(text_surface, pos)

    def render_text_centered(self, text, font, color, rect):
        # Renders text centered within the given rect
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(rect[0] + rect[2] // 2, rect[1] + rect[3] // 2))
        self.SCREEN.blit(text_surface, text_rect)

    def render_panel(self):
        # Render title
        self.SCREEN.blit(self.panel_bg,(0,0),(0,0,self.panel_width,self.window_height))
        font = pygame.font.SysFont(None, 36)
        #self.render_text("Lv.01", font, (0, 0, 0), (self.panel_width * 0.4, self.window_height * 0.05))
        self.render_text_centered("--- Lv.01 ---", font, (255, 255, 255), (0, self.window_height * 0.02, 200, 30))
        # Render buttons
        button_font = pygame.font.SysFont(None, 24)
        for i, pos in enumerate(self.button_positions):
            img = self.button_img
            if self.algorithm_buttons[i] == self.selected_algorithm:
                img = self.button_pressed_img
            button_rect = pygame.Rect(pos, (self.button_img.get_width(), self.button_img.get_height()*0.9))
            self.SCREEN.blit(img, pos)
            self.render_text_centered(self.algorithm_buttons[i], button_font, (0, 0, 0), button_rect)

        # Render ribbon and stats banner

        self.SCREEN.blit(self.banner_img, self.banner_position)
        self.SCREEN.blit(self.ribbon_img, self.ribbon_position)
        ribbon_rect = pygame.Rect(self.ribbon_position, (self.ribbon_img.get_width(), self.ribbon_img.get_height()*0.9))
        self.render_text_centered(self.selected_algorithm, pygame.font.SysFont(None, 24), (255, 255, 255), ribbon_rect)

        # Render stats text
        stats_font = pygame.font.SysFont(None, 20)
        self.render_text(f"Step: {self.current_state_index-1 if self.current_state_index>0 else 0}", stats_font, (0, 0, 0), (self.banner_position[0] + 15, self.banner_position[1] + ribbon_rect.height))
        self.render_text(f"Weight: 0", stats_font, (0, 0, 0), (self.banner_position[0] + 15, self.banner_position[1] + ribbon_rect.height+ 30))
        self.render_text(f"Node: {self.node_count.value}", stats_font, (0, 0, 0), (self.banner_position[0] + 15, self.banner_position[1] + ribbon_rect.height+ 60))
        self.render_text(f"Time: {self.time_taken.value:.3f}s", stats_font, (0, 0, 0), (self.banner_position[0] + 15, self.banner_position[1] + ribbon_rect.height+ 90))

        # Render control buttons
        self.SCREEN.blit(self.back_button_img, (self.panel_width * 0.1, self.window_height * 0.58))
        if self.pause:
            self.SCREEN.blit(self.pause_button_pressed_img, (self.panel_width * 0.37, self.window_height * 0.58))
        else:
            self.SCREEN.blit(self.pause_button_img, (self.panel_width * 0.37, self.window_height * 0.58))
        self.SCREEN.blit(self.reset_button_img, (self.panel_width * 0.64, self.window_height * 0.58))



        #Render result ribbon
        if self.flag_no_sol_found:
            result_width = 250
            result_height = 125
            result_x_center = 200+(self.window_width - 200)/2
            result_y_center = self.window_height/2
            result_rect = pygame.Rect(result_x_center,result_y_center,result_width,result_height)
            result_rect.center = (result_x_center,result_y_center)
            self.SCREEN.blit(self.result_ribbon,(result_rect.x,result_rect.y))
            self.render_text_centered('No Solution',stats_font,RED,result_rect)
        if self.flag_pass:
            result_width = 250
            result_height = 125
            result_x_center = 200 + (self.window_width - 200) / 2
            result_y_center = self.window_height / 2
            result_rect = pygame.Rect(result_x_center, result_y_center, result_width, result_height)
            result_rect.center = (result_x_center, result_y_center)
            self.SCREEN.blit(self.result_ribbon, (result_rect.x, result_rect.y))
            self.render_text_centered('Pass', font, GREEN, result_rect)
    def render_map(self,board: list[list[str]],char_direction:int):
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
                elif board[i][j] == '$':
                    center = self.rect_coord[i][j].center
                    img_rect = self.stone.get_rect()
                    img_rect.center = center
                    self.SCREEN.blit(self.stone, img_rect)
                elif board[i][j] == '@':
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

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            pause_button_rect = pygame.Rect(self.panel_width * 0.37, self.window_height * 0.58,
                                 self.panel_width * 0.25,self.panel_width * 0.25)
            reset_button_rect = pygame.Rect(self.panel_width * 0.64, self.window_height * 0.58,
                                            self.panel_width * 0.25, self.panel_width * 0.25)
            if pause_button_rect.collidepoint(mouse_x, mouse_y):
                self.pause = not self.pause
            if reset_button_rect.collidepoint(mouse_x,mouse_y):
                self.stop_current_algorithm()
                self.reset_state()
                self.selected_algorithm = None
            # Check for button clicks
            for i, pos in enumerate(self.button_positions):
                button_rect = pygame.Rect(pos, (self.button_img.get_width(), self.button_img.get_height()))
                if button_rect.collidepoint(mouse_x, mouse_y):
                    prev = self.selected_algorithm
                    self.selected_algorithm = self.algorithm_buttons[i]
                    if prev == self.selected_algorithm: continue
                    self.reset_state()
                    if self.selected_algorithm == 'A*':
                        a_star_instance = AStar(self.board, self.weight_list)
                        self.start_algorithm(a_star_instance.A_star)
                    elif self.selected_algorithm == 'UCS':
                        ucs_instance = UCS(self.board, self.weight_list)
                        self.start_algorithm(ucs_instance.UCS)
                    elif self.selected_algorithm == 'BFS':
                        bfs_instance = BFS(self.board)
                        self.start_algorithm(bfs_instance.BFS)
                    elif self.selected_algorithm == 'DFS':
                        dfs_instance = DFS(self.board)
                        self.start_algorithm(dfs_instance.DFS)
    def process_command(self, command: str, char_coord: tuple[int,int], board: list[list[str]]):
        map_dir = {
            'u': (-1, 0, 2),
            'd': (1, 0, 0),
            'l': (0, -1, 3),
            'r': (0, 1, 1)
        }
        if command.islower():
            char_x, char_y = char_coord
            change_x, change_y, char_direction = map_dir[command]
            new_board = deepcopy(board)
            new_board[char_x][char_y] = new_board[char_x][char_y].replace('@', '')
            new_board[char_x + change_x][char_y + change_y] = (new_board[char_x + change_x][char_y + change_y] + '@').strip()
            new_char_coord = (char_x + change_x, char_y + change_y)
            new_char_direction = char_direction
            return (new_board,new_char_coord,new_char_direction)
        else:
            char_x, char_y = char_coord
            change_x, change_y, char_direction = map_dir[command.lower()]
            stone_x, stone_y = char_x + change_x, char_y + change_y
            stone_x_after_push, stone_y_after_push = char_x + change_x * 2, char_y + change_y * 2
            new_board = deepcopy(board)
            if new_board[stone_x_after_push][stone_y_after_push] == '.':
                new_board[stone_x_after_push][stone_y_after_push] = '.$'
            else:
                new_board[stone_x_after_push][stone_y_after_push] = '$'
            new_board[stone_x][stone_y] = new_board[stone_x][stone_y].replace('$', '')
            new_board[stone_x][stone_y] = (new_board[stone_x][stone_y] + '@').strip()
            new_board[char_x][char_y] = new_board[char_x][char_y].replace('@', '')
            if new_board[char_x][char_y] == '':
                new_board[char_x][char_y] = ' '
            new_char_coord = (char_x + change_x, char_y + change_y)
            new_char_direction = char_direction
            return (new_board, new_char_coord, new_char_direction)
    def process_path_returned(self,path):
        board_states = []
        current_board = deepcopy(self.board)
        current_char_coord = self.char_coord
        current_char_dir = self.char_direction
        board_states.append((current_board, self.char_coord, self.char_direction))
        for ch in path:
            new_board,new_char_coord,new_char_dir = self.process_command(ch,current_char_coord,current_board)
            board_states.append((new_board,new_char_coord,new_char_dir))
            current_board = new_board
            current_char_coord = new_char_coord
            current_char_dir = new_char_dir
        return board_states
    def reset_state(self):
        self.current_state_index = -1
        self.path_shared.value = b""
        self.node_count.value = 0
        self.weight_pushed = 0
        self.time_taken.value = 0
        self.pause = False
        self.flag_no_sol_found = False
        self.flag_pass = False
    def stop_current_algorithm(self):
        if self.current_process and self.current_process.is_alive():
            self.stop_signal.set()  # Signal the process to stop
            self.current_process.join()  # Wait until process stops
            self.stop_signal.clear()  # Reset signal for future use
            self.current_process = None
            self.board_states = []
            self.reset_state()
            print("Algorithm stopped")

    def start_algorithm(self, algorithm_function):
        self.stop_current_algorithm()  # Stop any running algorithm
        self.current_process = multiprocessing.Process(target=algorithm_function, args=(self.time_taken,self.node_count, self.path_shared,self.stop_signal,))
        self.current_process.start()
    def visualize(self):
        run = True
        while (run):
            #print(self.node_count.value)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                else:
                    self.handle_event(event)

            if self.path_shared.value == b"":
                self.SCREEN.fill(GREEN)
                self.render_map(self.board, 0)
            elif self.path_shared.value == b"No solution found":
                self.flag_no_sol_found = True
            elif not self.pause:
                if self.current_state_index == -1:
                    path_returned = self.path_shared.value.decode()
                    self.board_states = self.process_path_returned(path_returned)
                    self.current_state_index = 0
                if self.current_state_index < len(self.board_states) and self.current_frame % self.frame_rate == 0:
                    current_board, current_char_coord, current_char_dir = self.board_states[self.current_state_index]
                    self.SCREEN.fill(GREEN)
                    self.render_map(current_board, current_char_dir)
                    self.current_state_index += 1
                if self.current_state_index == len(self.board_states):
                    self.flag_pass = True


            self.render_panel()

            pygame.display.flip()
            CLOCK.tick(self.frame_rate)
            self.current_frame += 1
#bfs = BFS(self.board)
#print(bfs.BFS())