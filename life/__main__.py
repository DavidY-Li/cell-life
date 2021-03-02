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
pygame.display.set_caption("Game of Life")

icon = pygame.image.load('glider.png')

pygame.display.set_icon(icon)

play = 0

generation = 0


def menu():
    global generation
    global play
    play = 0
    generation = 0
    board.clear_board()
    if board.playing == True:
        board.toggle_pause()


board = Board(
    width,
    height
)


def toggle_pause():
    board.toggle_pause()


def clear_board():
    global generation
    generation = 0
    board.clear_board()
    board.playing = False


def playground():
    global play
    play = 1

def multiplayer():
    global play
    play = 2

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
    on_click=menu,
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

playground_button = Button(
    colors.blue,
    colors.light_blue,
    680,
    400,
    400,
    125,
    "Playground",
    font=70,
    padding=0,
    on_click=playground,
)

multiplayer_button = Button(
    colors.red,
    colors.light_red,
    220,
    400,
    400,
    125,
    "Multiplayer",
    font=70,
    padding=0,
    on_click=multiplayer,
)

# Game loop
while True:

    # Game loop

    while play == 0:
        # Checking for user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            playground_button.handle_event(event)
            multiplayer_button.handle_event(event)

        screen.fill(colors.white)

        title_text = pygame.font.Font("pixel.ttf", 100).render(
            "Game of Life", 1, colors.black
        )
        title_rect = title_text.get_rect(center=(width / 2, 200))
        screen.blit(title_text, title_rect)

        playground_button.draw(screen)
        multiplayer_button.draw(screen)

        # Updating the display
        pygame.display.update()

        # Delay to save system resources
        pygame.time.wait(0)

    while play == 1:
        if board.playing:
            pause_button.text = "Pause"
            pause_button.set_width(120)
            generation += 1
            title_rect = title_text.get_rect(center=(680, 65))
        else:
            pause_button.text = "Play"
            pause_button.set_width(75)
            title_rect = title_text.get_rect(center=(635, 65))

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

        generation_rect = pygame.font.Font("pixel.ttf", 30).render(
            "Generation: " + str(generation), 1, colors.black
        )
        screen.blit(generation_rect, title_rect)

        board.next_step()

        # Updating the display
        pygame.display.update()

        # Delay to save system resources
        pygame.time.wait(0)

    while play == 2:
        if board.playing:
            pause_button.text = "Pause"
            pause_button.set_width(120)
            generation += 1
            title_rect = title_text.get_rect(center=(680, 65))
        else:
            pause_button.text = "Play"
            pause_button.set_width(75)
            title_rect = title_text.get_rect(center=(635, 65))

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

        generation_rect = pygame.font.Font("pixel.ttf", 30).render(
            "Generation: " + str(generation), 1, colors.black
        )
        screen.blit(generation_rect, title_rect)

        board.next_step()

        # Updating the display
        pygame.display.update()

        # Delay to save system resources
        pygame.time.wait(0)
