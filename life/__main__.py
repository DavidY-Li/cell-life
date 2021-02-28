import pygame
import sys
import random
from copy import deepcopy
from button import Button
from cell import Cell

# Screen size and initialization of pygame
pygame.init()
width, height = 1280, 720
size = [width, height]
screen = pygame.display.set_mode(size)

# Colors
black = [0, 0, 0]
white = [255, 255, 255]
red = [255, 0, 0]
light_red = [200, 10, 10]
grey = [200, 200, 200]
blue = [0, 30, 200]
light_blue = [0, 40, 255]

cell_width = 20

cells = [
    [Cell(False) for _ in range(int(width / cell_width))]
    for _ in range(int(height / cell_width))
]

play = 0
playing = False


def exit_pygame():
    pygame.quit()
    sys.exit()


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
    on_click=exit_pygame,
)


def toggle_pause():
    global playing
    playing = not playing


pause_button = Button(
    blue,
    light_blue,
    220,
    10,
    110,
    35,
    "Play",
    font=30,
    padding=0,
    on_click=toggle_pause,
)

def clear_board():
    global cells
    for row in cells:
        for col in row:
            col.set_alive(False)

clear_button = Button(
    blue,
    light_blue,
    100,
    10,
    110,
    35,
    "Clear",
    font=30,
    padding=0,
    on_click=clear_board,
)


def draw_grid():
    for x in range(height // cell_width):
        thickness = 1
        if x % 5 == 0:
            thickness = 2
        pygame.draw.line(screen, grey, (0, x * cell_width), (width, x * cell_width), thickness)
    for y in range(width // cell_width):
        thickness = 1
        if y % 5 == 0:
            thickness = 2
        pygame.draw.line(screen, grey, (y * cell_width, 0), (y * cell_width, height), thickness)


board_width, board_height = len(cells[0]), len(cells)
mouse_down = False
delete = False
previous = None

# Game loop
while True:

    # Game loop
    while play == 0:
        if playing:
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
            if event.type == pygame.MOUSEBUTTONDOWN:
                (x, y) = pygame.mouse.get_pos()
                (col, row) = (x // cell_width), (y // cell_width)
                clicked_cell = cells[row][col]
                delete = clicked_cell.is_alive()
                clicked_cell.set_alive(not clicked_cell.is_alive())
                mouse_down = True
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_down = False
            if event.type == pygame.MOUSEMOTION:
                if mouse_down:
                    (x, y) = pygame.mouse.get_pos()
                    (col, row) = (x // cell_width), (y // cell_width)
                    if (col, row) != previous:
                        clicked_cell = cells[row][col]
                        clicked_cell.set_alive(not delete)
                        previous = (col, row)

            game_back_button.handle_event(event)
            pause_button.handle_event(event)
            clear_button.handle_event(event)


        screen.fill(white)

        for (row_idx, row) in enumerate(cells):
            for (col_idx, val) in enumerate(row):
                if cells[row_idx][col_idx].is_alive():
                    pygame.draw.rect(
                        screen,
                        black,
                        [
                            col_idx * cell_width,
                            row_idx * cell_width,
                            cell_width,
                            cell_width,
                        ],
                    )

        if playing:
            new_cells = deepcopy(cells)
            for (row_idx, row) in enumerate(cells):
                for (col_idx, val) in enumerate(row):
                    surrounding = 0
                    for row_delta in [board_height - 1, 0, 1]:
                        for col_delta in [board_width - 1, 0, 1]:
                            if row_delta == 0 and col_delta == 0:
                                continue
                            changed_row = (row_idx + row_delta) % board_height
                            changed_col = (col_idx + col_delta) % board_width
                            surrounding += int(
                                cells[changed_row][changed_col].is_alive()
                            )
                    if (surrounding == 2 or surrounding == 3) and new_cells[row_idx][
                        col_idx
                    ].is_alive():
                        new_cells[row_idx][col_idx].set_alive(True)
                    elif (
                        surrounding == 3 and not new_cells[row_idx][col_idx].is_alive()
                    ):
                        new_cells[row_idx][col_idx].set_alive(True)
                    else:
                        new_cells[row_idx][col_idx].set_alive(False)
            cells = new_cells

        draw_grid()
        game_back_button.draw(screen)
        pause_button.draw(screen)
        clear_button.draw(screen)

        # Updating the display
        pygame.display.update()

        # Delay to save system resources
        #pygame.time.wait(0)
