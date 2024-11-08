import pygame
from globals import *

class MainScreen:
    def __init__(self):
        self.button_play_normal = pygame.transform.scale(pygame.image.load(r'resources/button/playNormal.png'),(200,100))
        self.button_play_hover = pygame.transform.scale(pygame.image.load(r'resources/button/playHover.png'),(200,100))
        self.background = pygame.transform.scale(pygame.image.load(r'resources/background/tile000.jpg'),(1200,800))
        self.window_width = 1200
        self.window_height = 800
        self.SCREEN = pygame.display.set_mode((self.window_width, self.window_height))
    def run(self):
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            self.SCREEN.fill(WHITE)
            self.SCREEN.blit(self.background,(0,0,self.window_width,self.window_height))
            self.SCREEN.blit(self.button_play_normal,(300,300,200,100))
            pygame.display.update()
            CLOCK.tick(60)