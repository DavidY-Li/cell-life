import pygame
from cell import Cell 
import colors
from copy import deepcopy

class Board:
    def __init__(self, width, height, playing=False, cell_width=20):
        self.cell_width = cell_width
        self.playing = playing
        self.cells = [
            [Cell(False) for _ in range(width // cell_width)]
            for _ in range(height // cell_width)
        ]
        self.width = width
        self.height = height
        self.board_width = width // cell_width
        self.board_height = height // cell_width
        self.mouse_down = False
        self.delete = False
        self.previous = None

    def toggle_pause(self):
        self.playing = not self.playing

    def draw(self, screen):
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

        for x in range(self.height // self.cell_width):
            thickness = 1
            if x % 5 == 0:
                thickness = 2
            pygame.draw.line(
                screen, colors.grey, (0, x * self.cell_width), (self.width, x * self.cell_width), thickness
            )
        for y in range(self.width // self.cell_width):
            thickness = 1
            if y % 5 == 0:
                thickness = 2
            pygame.draw.line(
                screen, colors.grey, (y * self.cell_width, 0), (y * self.cell_width, self.height), thickness
            )
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            (x, y) = pygame.mouse.get_pos()
            (col, row) = (x // self.cell_width), (y // self.cell_width)
            self.clicked_cell = self.cells[row][col]
            self.delete = self.clicked_cell.is_alive()
            self.clicked_cell.set_alive(not self.clicked_cell.is_alive())            
            self.mouse_down = True
        if event.type == pygame.MOUSEBUTTONUP:
            self.mouse_down = False
        if event.type == pygame.MOUSEMOTION:
            if self.mouse_down:
                (x, y) = pygame.mouse.get_pos()
                (col, row) = (x // self.cell_width), (y // self.cell_width)
                if (col, row) != self.previous:
                    self.clicked_cell = self.cells[row][col]
                    self.clicked_cell.set_alive(not self.delete)
                    self.previous = (col, row)

    def next_step(self):
        if self.playing:
            new_cells = deepcopy(self.cells)
            for (row_idx, row) in enumerate(self.cells):
                for (col_idx, _) in enumerate(row):
                    surrounding = 0
                    for row_delta in [self.board_height - 1, 0, 1]:
                        for col_delta in [self.board_width - 1, 0, 1]:
                            if row_delta == 0 and col_delta == 0:
                                continue
                            changed_row = (row_idx + row_delta) % self.board_height
                            changed_col = (col_idx + col_delta) % self.board_width
                            surrounding += int(
                                self.cells[changed_row][changed_col].is_alive()
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
            self.cells = new_cells

    def clear_board(self):
        for row in self.cells:
            for col in row:
                col.set_alive(False)