import pygame
import sys
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


cell_width = 20

play = 0


def print_test():
    print("test")


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

cells = [
    [Cell(False), Cell(False), Cell(False), Cell(False), Cell(False)],
    [Cell(False), Cell(False), Cell(False), Cell(False), Cell(False)],
    [Cell(False), Cell(False), Cell(True), Cell(False), Cell(False)],
    [Cell(False), Cell(False), Cell(True), Cell(False), Cell(False)],
    [Cell(False), Cell(False), Cell(True), Cell(False), Cell(False)],
    [Cell(False), Cell(False), Cell(False), Cell(False), Cell(False)],
    [Cell(False), Cell(False), Cell(False), Cell(False), Cell(False)],
]
board_width, board_height = len(cells[0]), len(cells)

# Game loop
while True:

    # Menu loop
    while play == 0:

        # Checking for user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(black)

        game_back_button.draw(screen)

        for (row_idx, row) in enumerate(cells):
            for (col_idx, val) in enumerate(row):
                if cells[row_idx][col_idx].is_alive():
                    pygame.draw.rect(
                        screen,
                        white,
                        [
                            col_idx * cell_width,
                            row_idx * cell_width,
                            cell_width,
                            cell_width,
                        ],
                    )

        for (row_idx, row) in enumerate(cells):
            for (col_idx, val) in enumerate(row):
                surrounding = 0
                print(f"{{({row_idx}, {col_idx}) -- ", end="")
                for row_delta in [board_height-1, 0, 1]:
                    for col_delta in [board_width-1, 0, 1]:
                        if row_delta == 0 and col_delta == 0:
                            continue
                        changed_row = row_idx + row_delta
                        changed_col = col_idx + col_delta
                        if row_delta != 0:
                            changed_row %= board_height
                        if col_delta != 0:
                            changed_col %= board_width
                        
                        if cells[changed_row][changed_col].is_alive():
                            surrounding += 1
                print(" --- }", surrounding, end="  ")
                if (surrounding == 2 or surrounding == 3) and cells[row_idx][
                    col_idx
                ].is_alive():
                    cells[row_idx][col_idx].set_alive(True)
                elif surrounding == 3 and not cells[row_idx][
                    col_idx
                ].is_alive():
                    cells[row_idx][col_idx].set_alive(True)
                else:
                    cells[row_idx][col_idx].set_alive(False)

            print()
        print()

        # Updating the display
        pygame.display.update()

        # Delay to save system resources
        pygame.time.wait(500)

    # Transition loop
    while play == 1:

        # Checking for user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(black)

        # Updating the display
        pygame.display.update()

        # Delay to save system resources
        pygame.time.wait(5)
