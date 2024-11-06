import pygame

class Button:
    def __init__(self, pos, text, font, base_color, hover_color, image = None):
        self.image = image
        self.x_pos, self.y_pos = pos
        self.font = font
        self.base_color = base_color
        self.hover_color = hover_color
        self.text = text
        self.current_color = base_color

        self.text_surface = self.font.render(self.text, True, self.current_color)
        if self.image:
            self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        else:
            self.rect = self.text_surface.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text_surface.get_rect(center=(self.x_pos, self.y_pos))

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, self.rect)
        screen.blit(self.text_surface, self.text_rect)

    def handle_event(self, event, mouse_pos):
        if self.is_hovered(mouse_pos):
            self.text_surface = self.font.render(self.text, True, self.hover_color)
        else:
            self.text_surface = self.font.render(self.text, True, self.base_color)

        if event.type == pygame.MOUSEBUTTONDOWN and self.is_hovered(mouse_pos):
            return True
        return False

    def is_hovered(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
