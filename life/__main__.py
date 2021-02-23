import pygame
import sys
from button import Button

# Screen size and initialization of pygame
pygame.init()
width, height = 1280, 720
size = [width, height]
screen = pygame.display.set_mode(size)

# Colors
black = [0, 0, 0]
red = [255, 0, 0]
light_red = [200, 10, 10]

play = 0

def print_test():
    print('test')

game_back_button = Button(
    red,
    light_red,
    15,
    10,
    75,
    35,
    "Exit",
    font=30,
    padding=0,
    on_click=print_test,
)

# Game loop
while True:

    # Menu loop
    while play == 0:

        # Checking for user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            game_back_button.handle_event(event)

        
        screen.fill(black)

        game_back_button.draw(screen)

        # Updating the display
        pygame.display.update()

        # Delay to save system resources
        pygame.time.wait(5)

    # Transition loop
    while play == 1:

        screen.fill(black)

        # Updating the display
        pygame.display.update()

        # Delay to save system resources
        pygame.time.wait(5)
