import pygame
import sys
import random
from button import Button
from cell import Cell
from board import Board
import colors

# Screen size and initialization of pygame
pygame.init()
width, height = 1280, 720
size = [width, height]
screen = pygame.display.set_mode(size)

play = 0

def exit_pygame():
    pygame.quit()
    sys.exit()

board = Board(
    width,
    height
)

def toggle_pause():
    board.toggle_pause()

def clear_board():
    board.clear_board()

game_back_button = Button(
    colors.red,
    colors.light_red,
    15,
    10,
    75,
    35,
    "Exit",
    font=30,
    padding=0,
    on_click=exit_pygame,
)

pause_button = Button(
    colors.blue,
    colors.light_blue,
    220,
    10,
    110,
    35,
    "Play",
    font=30,
    padding=0,
    on_click=toggle_pause,
)


clear_button = Button(
    colors.blue,
    colors.light_blue,
    100,
    10,
    110,
    35,
    "Clear",
    font=30,
    padding=0,
    on_click=clear_board,
)

# Game loop
while True:

    # Game loop
    while play == 0:
        if board.playing:
            pause_button.text = "Pause"
            pause_button.set_width(120)
        else:
            pause_button.text = "Play"
            pause_button.set_width(75)

        # Checking for user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            game_back_button.handle_event(event)
            pause_button.handle_event(event)
            clear_button.handle_event(event)
            board.handle_event(event)

        screen.fill(colors.white)

        board.draw(screen)

        game_back_button.draw(screen)
        pause_button.draw(screen)
        clear_button.draw(screen)

        board.next_step()

        # Updating the display
        pygame.display.update()

        # Delay to save system resources
        pygame.time.wait(0)
