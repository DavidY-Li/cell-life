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

icon = pygame.image.load("glider.png")

pygame.display.set_icon(icon)

play = 0

generation = 0

max_generation = 500

interval = 100


def menu():
    global generation
    global play
    global interval
    play = 0
    interval = 100
    generation = 0
    board.red = 0
    if board.playing:
        board.toggle_pause()


board = Board(width, height)


def toggle_pause():
    board.toggle_pause()
    if board.playing:
        board.reset()


def clear_board():
    global generation
    generation = 0
    board.red = 0
    board.clear_board()
    board.playing = False


def playground():
    global play
    board.clear_board()
    play = 2


def multiplayer():
    global play
    board.clear_board()
    board.red = 0
    play = 1


def reset():
    global generation
    board.load_reset()
    board.playing = False
    generation = 0


def show_help():
    global play
    play = 3


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
    340,
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

reset_button = Button(
    colors.red,
    colors.light_red,
    220,
    10,
    110,
    35,
    "Reset",
    font=30,
    padding=0,
    on_click=reset,
)

help_button = Button(
    colors.red,
    colors.light_red,
    10,
    10,
    110,
    35,
    "Rules",
    font=30,
    padding=0,
    on_click=show_help,
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
            help_button.handle_event(event)

        screen.fill(colors.white)

        title_text = pygame.font.Font("pixel.ttf", 100).render(
            "Game of Life", 1, colors.black
        )
        title_rect = title_text.get_rect(center=(width / 2, 200))
        screen.blit(title_text, title_rect)

        playground_button.draw(screen)
        multiplayer_button.draw(screen)
        help_button.draw(screen)

        # Updating the display
        pygame.display.update()

        # Delay to save system resources
        pygame.time.wait(0)

    # Multiplayer
    while play == 1:
        if board.playing:
            generation += 1

        # Checking for user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            game_back_button.handle_event(event)
            if generation != 500:
                board.handle_event(event)

        screen.fill(colors.white)

        board.draw(screen)

        if generation == interval - 1:
            board.playing = False
            generation += 1
            interval += 100

        if generation == max_generation:
            board.playing = False
            board.winner()
            if board.winner_color in "Red Wins!":
                winner = pygame.font.Font("pixel.ttf", 100).render(
                    board.winner_color, 1, colors.red
                )
            elif board.winner_color in "Blue Wins!":
                winner = pygame.font.Font("pixel.ttf", 100).render(
                    board.winner_color, 1, colors.blue
                )
            else:
                winner = pygame.font.Font("pixel.ttf", 100).render(
                    board.winner_color, 1, colors.black
                )
            winner_rect = winner.get_rect(center=(width / 2, 350))
            screen.blit(winner, winner_rect)

        game_back_button.draw(screen)

        title_rect = title_text.get_rect(center=(435, 65))
        generation_rect = pygame.font.Font("pixel.ttf", 30).render(
            "Generation: " + str(generation), 1, colors.black
        )
        screen.blit(generation_rect, title_rect)

        if not board.playing and generation < max_generation:
            if board.red < 15:
                turn = pygame.font.Font("pixel.ttf", 30).render(
                    "Red Turn: " + str(15 - board.red) + " Cells Left", 1, colors.red
                )
                turn_rect = turn.get_rect(center=(180, 700))
                screen.blit(turn, turn_rect)

            else:
                turn = pygame.font.Font("pixel.ttf", 30).render(
                    "Blue Turn: " + str(25 - board.red) + " Cells Left", 1, colors.blue
                )
                turn_rect = turn.get_rect(center=(180, 700))
                screen.blit(turn, turn_rect)

        board.next_step()

        # Updating the display
        pygame.display.update()

        # Delay to save system resources
        pygame.time.wait(0)

    # Single player
    while play == 2:
        if board.playing:
            pause_button.text = "Pause"
            pause_button.set_width(120)
            generation += 1
            title_rect = title_text.get_rect(center=(800, 65))
        else:
            pause_button.text = "Play"
            pause_button.set_width(75)
            title_rect = title_text.get_rect(center=(755, 65))

        # Checking for user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            game_back_button.handle_event(event)
            pause_button.handle_event(event)
            clear_button.handle_event(event)
            board.handle_event(event)
            reset_button.handle_event(event)

        screen.fill(colors.white)

        board.draw(screen)

        game_back_button.draw(screen)
        pause_button.draw(screen)
        clear_button.draw(screen)
        reset_button.draw(screen)

        generation_rect = pygame.font.Font("pixel.ttf", 30).render(
            "Generation: " + str(generation), 1, colors.black
        )
        screen.blit(generation_rect, title_rect)

        board.next_step()

        # Updating the display
        pygame.display.update()

        # Delay to save system resources
        pygame.time.wait(0)

    # Game info
    while play == 3:
        # Checking for user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            game_back_button.handle_event(event)

        screen.fill(colors.white)

        game_back_button.draw(screen)

        rules = pygame.font.Font("pixel.ttf", 100).render("Rules", 1, colors.black)
        rules_rect = rules.get_rect(center=(width / 2, 65))
        screen.blit(rules, rules_rect)

        rule1 = pygame.font.Font("pixel.ttf", 40).render("The Game of Life is different from any other game.", 1, colors.black)
        rule1_rect = rule1.get_rect(center=(width / 2, 135))
        screen.blit(rule1, rule1_rect)

        rule2 = pygame.font.Font("pixel.ttf", 40).render(" It is a game made of four simple rules and capable of", 1, colors.black)
        rule2_rect = rule2.get_rect(center=(width / 2, 180))
        screen.blit(rule2, rule2_rect)

        rule3 = pygame.font.Font("pixel.ttf", 40).render("simulating a Turing Machine. The rules are as follows:", 1, colors.black)
        rule3_rect = rule3.get_rect(center=(width / 2, 235))
        screen.blit(rule3, rule3_rect)

        rule4 = pygame.font.Font("pixel.ttf", 28).render("1. Any live cell with fewer than two live neighbours dies, as if by underpopulation.", 1, colors.black)
        rule4_rect = rule4.get_rect(center=(width / 2, 280))
        screen.blit(rule4, rule4_rect)

        rule5 = pygame.font.Font("pixel.ttf", 28).render("2. Any live cell with two or three live neighbours lives on to the next generation.", 1, colors.black)
        rule5_rect = rule5.get_rect(center=(width / 2, 325))
        screen.blit(rule5, rule5_rect)

        rule6 = pygame.font.Font("pixel.ttf", 28).render("3. Any live cell with more than three live neighbours dies, as if by overpopulation.", 1, colors.black)
        rule6_rect = rule6.get_rect(center=(width / 2, 370))
        screen.blit(rule6, rule6_rect)

        rule7 = pygame.font.Font("pixel.ttf", 28).render("4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.", 1, colors.black)
        rule7_rect = rule7.get_rect(center=(width / 2, 415))
        screen.blit(rule7, rule7_rect)


        # Updating the display
        pygame.display.update()

        # Delay to save system resources
        pygame.time.wait(0)
