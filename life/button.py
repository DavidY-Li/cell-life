import pygame

# Button class for easier generation of buttons
class Button:
    def __init__(
        self,
        primary,
        hover_color,
        x,
        y,
        width,
        height,
        text,
        font=18,
        padding=13,
        secondary_text="",
        on_click=None,
        font_color=[255, 255, 255],
    ):
        self.primary = primary
        self.hover_color = hover_color
        self.color = self.primary
        self.text = text
        self.on_click = on_click
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.secondary_text = secondary_text
        self.font = font
        self.font_color = font_color
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.padding = padding

    def set_width(self, width: int):
        self.width = width
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(
                screen,
                outline,
                (self.x - 2, self.y - 2, self.width + 4, self.height + 4),
                0,
            )

        # Drawing button rect
        pygame.draw.rect(screen, self.color, self.rect)

        # Placing primary text on button
        if self.text != "":
            font = pygame.font.Font("pixel.ttf", self.font)
            text = font.render(self.text, 1, self.font_color)
            screen.blit(
                text,
                (
                    self.x + (self.width / 2 - text.get_width() / 2),
                    self.y
                    + (self.height / 2 - text.get_height() / 2)
                    - self.padding
                    + 4,
                ),
            )

        # Placing secondary text on button with offset
        if self.secondary_text != "":
            font = pygame.font.Font("pixel.ttf", self.font)
            text = font.render(self.secondary_text, 1, self.font_color)
            screen.blit(
                text,
                (
                    self.x + (self.width / 2 - text.get_width() / 2),
                    self.y
                    + (self.height / 2 - text.get_height() / 2)
                    + self.font
                    + 5
                    - self.padding
                    + 4,
                ),
            )

    # Handling button click
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Gets mouse position
            mouse_pos = event.pos

            # Checks to see if the mouse pressed the button
            if self.rect.collidepoint(mouse_pos):
                if self.on_click != None:
                    self.on_click()
        elif event.type == pygame.MOUSEMOTION:
            # Gets mouse position
            mouse_pos = event.pos

            # Checks to see if the mouse pressed the button
            if self.rect.collidepoint(mouse_pos):
                self.color = self.hover_color
            else:
                self.color = self.primary