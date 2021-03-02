import pygame
from cell import Cell
import colors
from copy import deepcopy
import random


class Board:

    # Initial attributes
    def __init__(self, width, height, playing=False, cell_width=20):
        self.cell_width = cell_width
        self.playing = playing
        self.cells = [
            [Cell(False, colors.white) for _ in range(width // cell_width)]
            for _ in range(height // cell_width)
        ]
        self.width = width
        self.height = height
        self.board_width = width // cell_width
        self.board_height = height // cell_width
        self.mouse_down = False
        self.delete = False
        self.previous = None
        self.red = 0
        self.saved_copy = []

    # Toggles pause
    def toggle_pause(self):
        self.playing = not self.playing

    # Draws cells and grid on screen
    def draw(self, screen):
        # Nexted loop to draw every cell in every row and column
        for (row_idx, row) in enumerate(self.cells):
            for (col_idx, val) in enumerate(row):
                if val.is_alive():
                    pygame.draw.rect(
                        screen,
                        val.color,
                        [
                            col_idx * self.cell_width,
                            row_idx * self.cell_width,
                            self.cell_width,
                            self.cell_width,
                        ],
                    )

        # Draws grid in intervals
        for x in range(self.height // self.cell_width):
            thickness = 1
            if x % 5 == 0:
                thickness = 2
            pygame.draw.line(
                screen, colors.grey, (0, x * self.cell_width), (self.width,
                                                                x * self.cell_width), thickness
            )
        for y in range(self.width // self.cell_width):
            thickness = 1
            if y % 5 == 0:
                thickness = 2
            pygame.draw.line(
                screen, colors.grey, (y * self.cell_width, 0), (y *
                                                                self.cell_width, self.height), thickness
            )

    # Handles user input
    def handle_event(self, event):
        # Sets cell alive or dead based on position of click and current state of cell
        if event.type == pygame.MOUSEBUTTONDOWN:
            (x, y) = pygame.mouse.get_pos()
            (col, row) = (x // self.cell_width), (y // self.cell_width)
            self.clicked_cell = self.cells[row][col]
            self.delete = self.clicked_cell.is_alive()
            self.clicked_cell.set_alive(not self.clicked_cell.is_alive())
            if self.red < 10 and not self.playing:
                self.clicked_cell.color = colors.red
                self.red += 1
            elif self.red < 20 and not self.playing:
                self.clicked_cell.color = colors.blue
                self.red += 1
                if self.red == 20:
                    self.red = 0
                    self.playing = True
            self.mouse_down = True
            self.previous = (col, row)
        # Changes mouse state to unpressed after mouse button is unclicked
        if event.type == pygame.MOUSEBUTTONUP:
            self.mouse_down = False
        # Allows user to place with dragging
        if event.type == pygame.MOUSEMOTION:
            if self.mouse_down and not self.playing:
                (x, y) = pygame.mouse.get_pos()
                (col, row) = (x // self.cell_width), (y // self.cell_width)
                if (col, row) != self.previous:
                    self.clicked_cell = self.cells[row][col]
                    self.clicked_cell.set_alive(not self.delete)
                    if self.red < 10 and self.clicked_cell.color == colors.white:
                        self.clicked_cell.color = colors.red
                        self.red += 1
                    elif self.red < 20 and self.clicked_cell.color == colors.white:
                        self.clicked_cell.color = colors.blue
                        self.red += 1
                        if self.red == 20:
                            self.red = 0
                            self.playing = True
                    self.previous = (col, row)

    # Does next step of board
    def next_step(self):
        if self.playing:
            # Creates a deepcopy for original copy to be unaffected while cells change
            new_cells = deepcopy(self.cells)
            # Does new step for every part of board
            for (row_idx, row) in enumerate(self.cells):
                for (col_idx, _) in enumerate(row):
                    surrounding = 0
                    red_surrounding = 0
                    for row_delta in [self.board_height - 1, 0, 1]:
                        for col_delta in [self.board_width - 1, 0, 1]:
                            if row_delta == 0 and col_delta == 0:
                                continue
                            changed_row = (
                                row_idx + row_delta) % self.board_height
                            changed_col = (
                                col_idx + col_delta) % self.board_width
                            surrounding += int(
                                self.cells[changed_row][changed_col].is_alive()
                            )
                            red_surrounding += int(
                                self.cells[changed_row][changed_col].color == colors.red
                            )
                    # Any cell with two or three "neighbours" stays alive
                    if (surrounding == 2 or surrounding == 3) and new_cells[row_idx][
                        col_idx
                    ].is_alive():
                        new_cells[row_idx][col_idx].set_alive(True)
                    # Any dead cell with three "neighbours" becomes alive
                    elif (
                        surrounding == 3 and not new_cells[row_idx][col_idx].is_alive(
                        )
                    ):
                        new_cells[row_idx][col_idx].set_alive(True)
                        if red_surrounding > (surrounding / 2):
                            new_cells[row_idx][col_idx].color = colors.red
                        elif red_surrounding < (surrounding / 2):
                            new_cells[row_idx][col_idx].color = colors.blue
                        else:
                            new_cells[row_idx][col_idx].color = random.choice(
                                [colors.blue])
                    # All other cells die
                    else:
                        new_cells[row_idx][col_idx].set_alive(False)
                        new_cells[row_idx][col_idx].color = colors.white
            # Sets new cells to old cells
            self.cells = new_cells

    # Clear board function
    def clear_board(self):
        for row in self.cells:
            for col in row:
                col.set_alive(False)

    def reset(self):
        self.saved_copy = deepcopy(self.cells)

    def load_reset(self):
        if len(self.saved_copy) > 0:
            self.cells = self.saved_copy
