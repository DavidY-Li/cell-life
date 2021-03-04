import pygame
import sys
import random
from button import Button
from cell import Cell
import presets
from board import MultiplayerBoard, SingleplayerBoard, RainbowSingleplayerBoard
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

stats_written = False


def menu():
    global generation
    global play
    global interval
    global stats_written
    play = 0
    interval = 100
    generation = 0
    stats_written = False


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
    play = 4


def show_multiplayer_help():
    global play
    play = 5


def show_stats():
    global play
    play = 6


def rainbow_playground():
    global play
    play = 3


def rainbow_help():
    global play
    play = 7


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
    350,
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
    350,
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
    colors.blue,
    colors.light_blue,
    10,
    10,
    110,
    35,
    "Rules",
    font=30,
    padding=0,
    on_click=show_help,
)

multiplayer_help_button = Button(
    colors.red,
    colors.light_red,
    130,
    10,
    260,
    35,
    "Multiplayer Rules",
    font=30,
    padding=0,
    on_click=show_multiplayer_help,
)

stats_button = Button(
    colors.red,
    colors.light_red,
    1010,
    10,
    260,
    35,
    "Multiplayer Stats",
    font=30,
    padding=0,
    on_click=show_stats,
)

rainbow_button = Button(
    colors.hsv_to_rgb(1.0, 1, 1),
    colors.hsv_to_rgb(1.0, 0.5, 1),
    275,
    550,
    750,
    125,
    "Rainbow Playground",
    font=70,
    padding=0,
    on_click=rainbow_playground,
)

rainbow_help_button = Button(
    colors.hsv_to_rgb(1.0, 1, 1),
    colors.hsv_to_rgb(1.0, 0.5, 1),
    400,
    10,
    230,
    35,
    "Rainbow Help",
    font=30,
    padding=0,
    on_click=rainbow_help,
)

# Loads stats
stats = []
with open("stats.txt", "r") as f:
    for line in f.read().split("\n"):
        stats.append(int(line))

# Game loop
while True:

    # Game loop
    board = SingleplayerBoard(width, height, color=colors.dark_grey)
    board.cells = presets.glider_gun
    board.playing = True

    hue = 1.0
    rainbow_hovered = False
    rainbow_help_hovered = False
    while play == 0:
        # Shifts HSV value of rainbow buttons
        if not rainbow_hovered:
            rainbow_button.color = colors.hsv_to_rgb(hue, 1, 1)
            rainbow_button.primary = colors.hsv_to_rgb(hue, 1, 1)
        else:
            rainbow_button.color = colors.hsv_to_rgb(hue, 0.5, 1)
            rainbow_button.primary = colors.hsv_to_rgb(hue, 0.5, 1)

        if not rainbow_help_hovered:
            rainbow_help_button.color = colors.hsv_to_rgb(hue, 1, 1)
            rainbow_help_button.primary = colors.hsv_to_rgb(hue, 1, 1)
        else:
            rainbow_help_button.color = colors.hsv_to_rgb(hue, 0.5, 1)
            rainbow_help_button.primary = colors.hsv_to_rgb(hue, 0.5, 1)

        rainbow_button.hover_color = colors.hsv_to_rgb(hue, 0.5, 1)
        rainbow_help_button.hover_color = colors.hsv_to_rgb(hue, 0.5, 1)

        hue -= 0.003
        hue %= 1.0

        board.next_step()

        # Checking for user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            playground_button.handle_event(event)
            multiplayer_button.handle_event(event)
            help_button.handle_event(event)
            multiplayer_help_button.handle_event(event)
            stats_button.handle_event(event)
            rainbow_button.handle_event(event)
            rainbow_help_button.handle_event(event)
            if event.type == pygame.MOUSEMOTION:
                # Gets mouse position
                mouse_pos = event.pos
                rainbow_hovered = rainbow_button.rect.collidepoint(mouse_pos)
                rainbow_help_hovered = rainbow_help_button.rect.collidepoint(mouse_pos)

        screen.fill(colors.white)

        board.draw(screen)

        title_text = pygame.font.Font("pixel.ttf", 100).render(
            "Game of Life", 1, colors.black
        )
        title_rect = title_text.get_rect(center=(width / 2, 200))
        screen.blit(title_text, title_rect)

        playground_button.draw(screen)
        multiplayer_button.draw(screen)
        help_button.draw(screen)
        multiplayer_help_button.draw(screen)
        stats_button.draw(screen)
        rainbow_button.draw(screen)
        rainbow_help_button.draw(screen)

        # Updating the display
        pygame.display.update()

        # Delay to save system resources
        pygame.time.wait(0)

    board = MultiplayerBoard(width, height)

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
                if stats_written == False:
                    stats[3] = int(stats[3] + 1)
            elif board.winner_color in "Blue Wins!":
                winner = pygame.font.Font("pixel.ttf", 100).render(
                    board.winner_color, 1, colors.blue
                )
                if stats_written == False:
                    stats[2] = int(stats[2] + 1)
            else:
                winner = pygame.font.Font("pixel.ttf", 100).render(
                    board.winner_color, 1, colors.black
                )
            # Writes stats to file
            if stats_written == False:

                stats[0] = int(stats[0] + 10 * max_generation / 100)
                stats[1] = int(stats[1] + 15 * max_generation / 100)
                stats[4] = int(stats[4] + max_generation)
                stats[5] = int(stats[5] + 1)

                with open("stats.txt", "w") as f:
                    f.write("\n".join(map(str, stats)))

                stats_written = True

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

        # No delay to allow more cell placements per second
        pygame.time.wait(0)

    board = SingleplayerBoard(width, height)

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

        # No delay to allow more cell placements per second
        pygame.time.wait(0)

    board = RainbowSingleplayerBoard(width, height)

    # Single player rainbow
    while play == 3:
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

        # No delay to allow more cell placements per second
        pygame.time.wait(0)

    # Game info
    while play == 4:
        # Checking for user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            game_back_button.handle_event(event)

        screen.fill(colors.white)

        board.draw(screen)

        game_back_button.draw(screen)

        # Game info text
        rules = pygame.font.Font("pixel.ttf", 100).render("Rules", 1, colors.black)
        rules_rect = rules.get_rect(center=(width / 2, 65))
        screen.blit(rules, rules_rect)

        rule1 = pygame.font.Font("pixel.ttf", 40).render(
            "The Game of Life is different from any other game.", 1, colors.black
        )
        rule1_rect = rule1.get_rect(center=(width / 2, 135))
        screen.blit(rule1, rule1_rect)

        rule2 = pygame.font.Font("pixel.ttf", 40).render(
            "It is a game made of four simple rules and capable of", 1, colors.black
        )
        rule2_rect = rule2.get_rect(center=(width / 2, 180))
        screen.blit(rule2, rule2_rect)

        rule3 = pygame.font.Font("pixel.ttf", 40).render(
            "simulating a Turing Machine. The rules are as follows:", 1, colors.black
        )
        rule3_rect = rule3.get_rect(center=(width / 2, 225))
        screen.blit(rule3, rule3_rect)

        rule4 = pygame.font.Font("pixel.ttf", 28).render(
            "1. Any live cell with fewer than two live neighbours dies, as if by underpopulation.",
            1,
            colors.black,
        )
        rule4_rect = rule4.get_rect(center=(width / 2, 320))
        screen.blit(rule4, rule4_rect)

        rule5 = pygame.font.Font("pixel.ttf", 28).render(
            "2. Any live cell with two or three live neighbours lives on to the next generation.",
            1,
            colors.black,
        )
        rule5_rect = rule5.get_rect(center=(width / 2, 420))
        screen.blit(rule5, rule5_rect)

        rule6 = pygame.font.Font("pixel.ttf", 28).render(
            "3. Any live cell with more than three live neighbours dies, as if by overpopulation.",
            1,
            colors.black,
        )
        rule6_rect = rule6.get_rect(center=(width / 2, 520))
        screen.blit(rule6, rule6_rect)

        rule7 = pygame.font.Font("pixel.ttf", 28).render(
            "4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.",
            1,
            colors.black,
        )
        rule7_rect = rule7.get_rect(center=(width / 2, 620))
        screen.blit(rule7, rule7_rect)

        # Updating the display
        pygame.display.update()

        # Delay to save system resources
        pygame.time.wait(10)

    # Multiplayer info
    while play == 5:
        # Checking for user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            game_back_button.handle_event(event)

        screen.fill(colors.white)

        board.draw(screen)

        game_back_button.draw(screen)

        # Multiplayer info text
        rules = pygame.font.Font("pixel.ttf", 100).render(
            "Multiplayer Rules", 1, colors.black
        )
        rules_rect = rules.get_rect(center=(width / 2, 65))
        screen.blit(rules, rules_rect)

        rule1 = pygame.font.Font("pixel.ttf", 30).render(
            "1. Every 100 generations, both players are allowed to place new cells.",
            1,
            colors.black,
        )
        rule1_rect = rule1.get_rect(center=(width / 2, 180))
        screen.blit(rule1, rule1_rect)

        rule2 = pygame.font.Font("pixel.ttf", 30).render(
            "2. New cells inherit colors from the most common colors around them",
            1,
            colors.black,
        )
        rule2_rect = rule2.get_rect(center=(width / 2, 280))
        screen.blit(rule2, rule2_rect)

        rule3 = pygame.font.Font("pixel.ttf", 30).render(
            "3. The winner of the game the most common color after 500 generations.",
            1,
            colors.black,
        )
        rule3_rect = rule3.get_rect(center=(width / 2, 380))
        screen.blit(rule3, rule3_rect)

        rule4 = pygame.font.Font("pixel.ttf", 30).render(
            "4. All other rules remain the same.",
            1,
            colors.black,
        )
        rule4_rect = rule4.get_rect(center=(width / 2, 480))
        screen.blit(rule4, rule4_rect)

        tip1 = pygame.font.Font("pixel.ttf", 30).render(
            "Red gets 15 cells per 100 generation while blue gets 10. Because red goes",
            1,
            colors.black,
        )
        tip1_rect = tip1.get_rect(center=(width / 2 + 30, 580))
        screen.blit(tip1, tip1_rect)

        tip2 = pygame.font.Font("pixel.ttf", 30).render(
            "first, this is done to prevent blue from immediatly stopping red cells.",
            1,
            colors.black,
        )
        tip2_rect = tip2.get_rect(center=(width / 2, 630))
        screen.blit(tip2, tip2_rect)

        tip = pygame.font.Font("pixel.ttf", 30).render(
            "Tip:",
            1,
            colors.red,
        )
        tip_rect = tip.get_rect(center=(109, 580))
        screen.blit(tip, tip_rect)

        # Updating the display
        pygame.display.update()

        # Delay to save system resources
        pygame.time.wait(10)

    # Stats button
    while play == 6:
        # Checking for user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            game_back_button.handle_event(event)

        screen.fill(colors.white)

        board.draw(screen)

        game_back_button.draw(screen)

        # Stats text
        stats_title = pygame.font.Font("pixel.ttf", 100).render(
            "Multiplayer Stats", 1, colors.black
        )
        stats_rect = stats_title.get_rect(center=(width / 2, 65))
        screen.blit(stats_title, stats_rect)

        rendered_stats = pygame.font.Font("pixel.ttf", 80).render(
            "Multiplayer Games Played: " + str(stats[5]), 1, colors.black
        )
        highscore_rect = rendered_stats.get_rect(center=(width / 2, 160))
        screen.blit(rendered_stats, highscore_rect)

        rendered_stats = pygame.font.Font("pixel.ttf", 80).render(
            "Generations Played: " + str(stats[4]), 1, colors.black
        )
        highscore_rect = rendered_stats.get_rect(center=(width / 2, 250))
        screen.blit(rendered_stats, highscore_rect)

        rendered_stats = pygame.font.Font("pixel.ttf", 80).render(
            "Red Wins: " + str(stats[3]), 1, colors.red
        )
        highscore_rect = rendered_stats.get_rect(center=(width / 2, 340))
        screen.blit(rendered_stats, highscore_rect)

        rendered_stats = pygame.font.Font("pixel.ttf", 80).render(
            "Blue Wins: " + str(stats[2]), 1, colors.blue
        )
        highscore_rect = rendered_stats.get_rect(center=(width / 2, 430))
        screen.blit(rendered_stats, highscore_rect)

        rendered_stats = pygame.font.Font("pixel.ttf", 80).render(
            "Red Cells Placed: " + str(stats[1]), 1, colors.red
        )
        highscore_rect = rendered_stats.get_rect(center=(width / 2, 520))
        screen.blit(rendered_stats, highscore_rect)

        rendered_stats = pygame.font.Font("pixel.ttf", 80).render(
            "Blue Cells Placed: " + str(stats[0]), 1, colors.blue
        )
        highscore_rect = rendered_stats.get_rect(center=(width / 2, 610))
        screen.blit(rendered_stats, highscore_rect)

        # Updating the display
        pygame.display.update()

        # Delay to save system resources
        pygame.time.wait(10)

    # Rainbow playground rules
    while play == 7:
        # Checking for user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            game_back_button.handle_event(event)

        screen.fill(colors.white)

        board.draw(screen)

        game_back_button.draw(screen)

        # Playground info text
        rules = pygame.font.Font("pixel.ttf", 100).render(
            "Rainbow Rules", 1, colors.black
        )
        rules_rect = rules.get_rect(center=(width / 2, 65))
        screen.blit(rules, rules_rect)

        rule1 = pygame.font.Font("pixel.ttf", 40).render(
            "1. Colors are chosen randomly between red, green, and blue.",
            1,
            colors.black,
        )
        rule1_rect = rule1.get_rect(center=(width / 2, 180))
        screen.blit(rule1, rule1_rect)

        rule2 = pygame.font.Font("pixel.ttf", 40).render(
            "2. New cells inherit their colors from surrounding cells.",
            1,
            colors.black,
        )
        rule2_rect = rule2.get_rect(center=(width / 2, 280))
        screen.blit(rule2, rule2_rect)

        rule3 = pygame.font.Font("pixel.ttf", 40).render(
            "3. All other rules remain the same.",
            1,
            colors.black,
        )
        rule3_rect = rule3.get_rect(center=(width / 2, 380))
        screen.blit(rule3, rule3_rect)

        # Updating the display
        pygame.display.update()

        # Delay to save system resources
        pygame.time.wait(10)