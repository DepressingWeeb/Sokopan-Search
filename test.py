import pygame
import sys
from MainMenu import MainMenu


# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Sokoban Game")

# Screen States
MAIN_MENU = "main_menu"
LEVEL_SELECTION = "level_selection"
VISUALIZER = "visualizer"
current_screen = MAIN_MENU

# Screen Instances
main_menu = MainMenu(screen)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            if current_screen == MAIN_MENU:
                start_button = main_menu.display()
