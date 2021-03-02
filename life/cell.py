import random
import colors

class Cell:
    def __init__(self, alive: bool, color):
        self.color = color
        self._alive = alive

    def is_alive(self):
        return self._alive

    def set_alive(self, new_alive: bool):
        self._alive = new_alive