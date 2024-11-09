import sys

import pygame

import utils
import visulizer

Level_size =(1280,720)
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

    def scale_text(self, text, button_height):
        # Scale the font size based on the button's height (adjust the divisor as needed)
        font_size = max(10, int(button_height * 0.3))  # 0.5 is an arbitrary scale factor for readability
        scaled_font = get_font(font_size)  # You can pass the font path if needed
        return scaled_font.render(text, True, (255, 255, 255))
    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if self.rect.collidepoint(position):
            return True
        return False

    def changeColor(self, position):
        if self.rect.collidepoint(position):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)
class LevelButton:
    def __init__(self, pos, size, text, font, level_number, image=None):
        # Set up the button rectangle and level number
        self.rect = pygame.Rect(pos, size)
        self.level_number = level_number
        self.image = pygame.transform.scale(image, size) if image else None

        # Dynamically set the font size based on the button height
        self.text = self.scale_text(text, size[1])
        self.text_rect = self.text.get_rect()
        self.text_rect.x = self.rect.x + 40  # Offset by 10 pixels from left
        self.text_rect.y = self.rect.y + 40

    def scale_text(self, text, button_height):
        # Scale the font size based on the button's height (adjust the divisor as needed)
        font_size = max(10, int(button_height * 0.25))  # 0.5 is an arbitrary scale factor for readability
        scaled_font = get_font(font_size) # You can pass the font path if needed
        return scaled_font.render(text, True, (255, 255, 255))  # White color

    def draw(self, screen):
        # Draw the button image or default background
        if self.image:
            screen.blit(self.image, self.rect)  # Draw button image
        else:
            pygame.draw.rect(screen, (50, 50, 50), self.rect)  # Default button background
        # Draw the text centered in the button
        screen.blit(self.text, self.text_rect)

    def is_clicked(self, pos):
        # Check if the button was clicked
        return self.rect.collidepoint(pos)

class LevelSelectionScreen:
        def __init__(self, screen, font, num_levels=10):
            self.screen = screen
            self.font = font
            self.num_levels = num_levels
            self.buttons = []
            self.load_buttons()
            self.back_button = Button(
                image=pygame.image.load("resources/ui/back_icon.png"),  # Your back button image
                pos=(80, 80),  # Position in the upper-right corner
                text_input="",
                font=self.font,
                base_color="#d7fcd4",
                hovering_color="White",
                scale=(72,72)  # Adjusted size of the button
            )
            self.background_image = pygame.image.load("resources/ui/background.png")
            self.background_image = pygame.transform.scale(self.background_image, Level_size)

            self.title_image = pygame.image.load("resources/ui/Ribbon.png")
            self.title_image = pygame.transform.scale(self.title_image, (400, 120))
            self.title_rect = self.title_image.get_rect(center=(screen.get_width() // 2, 80))

        # Render text on the title image
            self.title_text = self.title_text = self.get_scaled_font("Level", self.title_image.get_width()-100, initial_font_size=48)
            self.title_text_rect = self.title_text.get_rect(center=self.title_rect.center)

        def get_scaled_font(self, text, max_width, initial_font_size=50, font_name="resources/ui/font.ttf",
                                color=(255, 255, 255)):
                font_size = initial_font_size  # Start with a large font size
                font = pygame.font.Font(font_name, font_size)
                rendered_text = font.render(text, True, color)
                # Keep reducing the font size until the text fits within the max_width
                while rendered_text.get_width() > max_width-30 and font_size > 10:  # Set a minimum font size to avoid going too small
                    font_size -= 1
                    font = pygame.font.Font(font_name, font_size)
                    rendered_text = font.render(text, True, color)
                return rendered_text
        def load_buttons(self):
            rows, cols = 2, 5  # Adjust as needed
            button_size = (150, 150)
            start_x, start_y = 75, 200
            gapX = 100
            gapY = 50
            level = 1
            for row in range(rows):
                for col in range(cols):
                    if level > self.num_levels:
                        break
                    x = start_x + col * (button_size[0] + gapX)
                    y = start_y + row * (button_size[1] + gapY)
                    button = LevelButton((x, y), button_size, f"{level:02}", self.font, level,
                                         image=pygame.image.load("resources/ui/Button.png"))
                    self.buttons.append(button)
                    level += 1


        def display(self):
                self.screen.blit(self.background_image, (0, 0))
                self.screen.blit(self.title_image, self.title_rect)
                self.screen.blit(self.title_text, self.title_text_rect)
                mouse_pos = pygame.mouse.get_pos()
                # Draw all level buttons
                for button in self.buttons:
                    button.draw(self.screen)
                self.back_button.changeColor(mouse_pos)
                self.back_button.update(self.screen)
        def handle_event(self, event):
                mouse_pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:  # Left click
                            level_number = self.handle_click(mouse_pos)
                            if level_number is not None:
                                return level_number
                            elif self.back_button.checkForInput(mouse_pos):
                                 return "MainMenu"
        def handle_click(self, pos):
            for button in self.buttons:
                if button.is_clicked(pos):
                    return button.level_number
            return None
