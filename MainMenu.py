import pygame, sys
import pygame

# Load assets
def get_font(size):
    return pygame.font.Font("resources/ui/font.ttf", size)

class Button:
    def __init__(self, image, pos, text_input, font, base_color, hovering_color, scale=None):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)

        # Scale image if a scale is provided
        if self.image is not None and scale is not None:
            self.image = pygame.transform.scale(self.image, scale)

        # Use text as image if no image is provided
        if self.image is None:
            self.image = self.text

        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos+5, self.y_pos - 5))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        return self.rect.collidepoint(position)

    def changeColor(self, position):
        if self.rect.collidepoint(position):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

class MainMenu:
    def __init__(self, game):
        self.game = game
        self.bg = pygame.transform.scale(pygame.image.load("resources/ui/background.png"),(1280,720))
        self.title_font = get_font(100)
        self.button_font = get_font(50)
        self.play_button = Button(
            image=pygame.image.load("resources/ui/Button_3Slides.png"),
            pos=(self.game.screen_width // 2, self.game.screen_height // 2 - 50),
            text_input="PLAY",
            font=self.button_font,
            base_color="#d7fcd4",
            hovering_color="White",
            scale=(300, 150)
        )


    def display(self):
        # Draw background and title
        self.game.screen.blit(self.bg, (0, 0))
        title_text = self.title_font.render("SOKOBAN", True, "#FFFFFF")
        title_rect = title_text.get_rect(center=(self.game.screen_width // 2, 150))
        self.game.screen.blit(title_text, title_rect)

        # Update and draw buttons
        self.play_button.changeColor(pygame.mouse.get_pos())
        self.play_button.update(self.game.screen)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.play_button.checkForInput(mouse_pos):
                return "level_selection_screen"