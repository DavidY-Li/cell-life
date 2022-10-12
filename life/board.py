import pygame
from cell import Cell
import colors
from copy import deepcopy
import random
import colorsys


class Board:
    # Initial attributes
    def __init__(self, width, height, playing=False, cell_width=20):
        """A board represents a Conway's game of life world."""
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
                screen,
                colors.grey,
                (0, x * self.cell_width),
                (self.width, x * self.cell_width),
                thickness,
            )
        for y in range(self.width // self.cell_width):
            thickness = 1
            if y % 5 == 0:
                thickness = 2
            pygame.draw.line(
                screen,
                colors.grey,
                (y * self.cell_width, 0),
                (y * self.cell_width, self.height),
                thickness,
            )

    # Handles user input
    def handle_event(self, event):
        # Sets cell alive or dead based on position of click and current state of cell
        if event.type == pygame.MOUSEBUTTONDOWN:
            (x, y) = pygame.mouse.get_pos()
            (col, row) = (x // self.cell_width), (y // self.cell_width)
            self.clicked_cell = self.cells[row][col]
            self.delete = self.clicked_cell.is_alive()
            self.handle_click()
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
                    self.handle_drag()
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
                    surrounding_color = []
                    for row_delta in [self.board_height - 1, 0, 1]:
                        for col_delta in [self.board_width - 1, 0, 1]:
                            if row_delta == 0 and col_delta == 0:
                                continue
                            changed_row = (row_idx + row_delta) % self.board_height
                            changed_col = (col_idx + col_delta) % self.board_width
                            surrounding += int(
                                self.cells[changed_row][changed_col].is_alive()
                            )
                            red_surrounding += int(
                                self.cells[changed_row][changed_col].color == colors.red
                            )
                            if self.cells[changed_row][changed_col].is_alive():
                                surrounding_color.append(
                                    self.cells[changed_row][changed_col].color
                                )
                    # Any cell with two or three "neighbours" stays alive
                    if (surrounding == 2 or surrounding == 3) and new_cells[row_idx][
                        col_idx
                    ].is_alive():
                        new_cells[row_idx][col_idx].set_alive(True)
                    # Any dead cell with three "neighbours" becomes alive
                    elif (
                        surrounding == 3 and not new_cells[row_idx][col_idx].is_alive()
                    ):
                        new_cells[row_idx][col_idx].set_alive(True)
                        self.set_new_color(
                            red_surrounding,
                            surrounding,
                            new_cells,
                            row_idx,
                            col_idx,
                            surrounding_color,
                        )
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
                col.color = colors.white

    # Creates a save of current board
    def reset(self):
        self.saved_copy = deepcopy(self.cells)

    # Loads previous board
    def load_reset(self):
        if len(self.saved_copy) > 0:
            self.cells = self.saved_copy

    # Determines winner based on number of cells
    def winner(self):
        red = 0
        blue = 0
        for row in self.cells:
            for val in row:
                if val.color == colors.red:
                    red += 1
                if val.color == colors.blue:
                    blue += 1
        if red < blue:
            self.winner_color = "Blue Wins!"
        elif red > blue:
            self.winner_color = "Red Wins!"
        else:
            self.winner_color = "Tie"

    # Overrides default board methods
    def handle_drag(self):
        raise Exception("Default")

    def handle_click(self):
        raise Exception("Default")

    def set_new_color(
        self,
        red_surrounding,
        surrounding,
        new_cells,
        row_idx,
        col_idx,
        surrounding_color,
    ):
        raise Exception("Default")


# Multiplayer board class that inherits from main board class
class MultiplayerBoard(Board):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.red = 0
        self.winner_color = ""

    # Drag place method for multiplayer
    def handle_drag(self):
        if (
            self.clicked_cell.is_alive()
            and self.delete
            and (
                (
                    self.clicked_cell.color == colors.red
                    and self.red < 15
                    and self.red > 0
                )
                or (self.clicked_cell.color == colors.blue and self.red > 15)
            )
        ):
            self.clicked_cell.set_alive(not self.delete)
            self.clicked_cell.color = colors.white
            self.red -= 1
        elif (
            not self.clicked_cell.is_alive() and self.clicked_cell.color == colors.white
        ):
            self.clicked_cell.set_alive(not self.delete)

        if (
            self.red < 15
            and not self.playing
            and self.clicked_cell.color == colors.white
            and not self.delete
        ):
            self.clicked_cell.color = colors.red
            self.red += 1
        elif (
            self.red >= 15
            and not self.playing
            and self.clicked_cell.color == colors.white
            and not self.delete
        ):
            self.clicked_cell.color = colors.blue
            self.red += 1
            if self.red == 25:
                self.red = 0
                self.playing = True

    # Click place method for multiplayer
    def handle_click(self):
        if (
            self.clicked_cell.is_alive()
            and not self.playing
            and (
                (
                    self.clicked_cell.color == colors.red
                    and self.red < 15
                    and self.red > 0
                )
                or (self.clicked_cell.color == colors.blue and self.red > 15)
            )
        ):
            self.clicked_cell.set_alive(not self.clicked_cell.is_alive())
            self.clicked_cell.color = colors.white
            self.red -= 1
        elif (
            not self.clicked_cell.is_alive() and self.clicked_cell.color == colors.white
        ):
            self.clicked_cell.set_alive(not self.clicked_cell.is_alive())

        if (
            self.red < 15
            and not self.playing
            and self.clicked_cell.is_alive()
            and self.clicked_cell.color == colors.white
        ):
            self.clicked_cell.color = colors.red
            self.red += 1
        elif (
            self.red >= 15
            and not self.playing
            and self.clicked_cell.is_alive()
            and self.clicked_cell.color == colors.white
        ):
            self.clicked_cell.color = colors.blue
            self.red += 1
            if self.red == 25:
                self.red = 0
                self.playing = True

    # New color method
    # Color of a new cell is the most common color of other cells around it
    def set_new_color(
        self,
        red_surrounding,
        surrounding,
        new_cells,
        row_idx,
        col_idx,
        surrounding_color,
    ):
        if red_surrounding > (surrounding / 2):
            new_cells[row_idx][col_idx].color = colors.red
        elif red_surrounding < (surrounding / 2):
            new_cells[row_idx][col_idx].color = colors.blue
        else:
            new_cells[row_idx][col_idx].color = random.choice([colors.blue, colors.red])


# Singleplayer board class that inherits from main board class
class SingleplayerBoard(Board):
    def __init__(self, *args, color=colors.black, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = color

    # Drag place method for singleplayer
    def handle_drag(self):
        self.clicked_cell.set_alive(not self.delete)
        self.clicked_cell.color = self.color

    # Click place method for singleplayer
    def handle_click(self):
        self.clicked_cell.set_alive(not self.clicked_cell.is_alive())
        self.clicked_cell.color = self.color

    # New color method
    # Color of new cells is always black
    def set_new_color(
        self,
        red_surrounding,
        surrounding,
        new_cells,
        row_idx,
        col_idx,
        surrounding_color,
    ):
        new_cells[row_idx][col_idx].color = self.color


# Rainbow singleplayer board class that inherits from main board class
class RainbowSingleplayerBoard(Board):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # Drag place method for rainbow singleplayer
    def handle_drag(self):
        self.clicked_cell.set_alive(not self.delete)
        self.clicked_cell.color = random.choice([colors.red, colors.green, colors.blue])

    # Click place method for rainbow singleplayer
    def handle_click(self):
        self.clicked_cell.set_alive(not self.clicked_cell.is_alive())
        self.clicked_cell.color = random.choice([colors.red, colors.green, colors.blue])

    # New color method
    # Color of new cells is based on average color of other cells around it
    # The color is first converted to HSV in order to keep the color fully saturated
    def set_new_color(
        self,
        red_surrounding,
        surrounding,
        new_cells,
        row_idx,
        col_idx,
        surrounding_color,
    ):
        red_value = 0
        green_value = 0
        blue_value = 0
        hsv_color = []

        for color in surrounding_color:
            red_value += color[0]
        red_value /= len(surrounding_color)

        for color in surrounding_color:
            green_value += color[1]
        green_value /= len(surrounding_color)

        for color in surrounding_color:
            blue_value += color[2]
        blue_value /= len(surrounding_color)

        hsv_color = colors.rgb_to_hsv(red_value, blue_value, green_value)

        new_cells[row_idx][col_idx].color = colors.hsv_to_rgb(hsv_color[0], 1, 1)
