import pygame, sys

import visulizer
from MainMenu import MainMenu
from Level import LevelSelectionScreen
import utils

# Initialize pygame and create constants

# Load assets
Level_size =(1280,720)
def get_font(size):
    return pygame.font.Font("resources/ui/font.ttf", size)

# Button and screen classes omitted for brevity; assuming they’re the same as the previous code
class Game:
    def __init__(self):
        pygame.init()
        self.screen_width, self.screen_height = 1280, 720
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.font = get_font(50)
        self.main_menu = MainMenu(self)
        self.level_selection_screen = LevelSelectionScreen(self.screen, self.font)
        self.screen_stack = [self.main_menu]  # Start with main menu
        pygame.display.set_caption("Game")
    def run(self):
        while True:
            current_screen = self.screen_stack[-1]  # Get the current screen from the stack
            current_screen.display()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                result=current_screen.handle_event(event)
            if result == "level_selection_screen":
                self.screen_stack.append(self.level_selection_screen)
            elif result == "MainMenu":
                if len(self.screen_stack) > 1:
                    self.screen_stack.pop()
            elif isinstance(result,int):
                board_inp, weight_list_inp = utils.input_txt_file(f'levels/input_{result}.txt')
                result = visulizer.Visualizer(board_inp, weight_list_inp)
                result.visualize()
                if result =="back_level_selection_screen":
                    self.screen_stack.append(self.level_selection_screen)

            pygame.display.update()
if __name__ == "__main__":
    game = Game()
    game.run()