class Cell:
    def __init__(self, alive: bool):
        self._alive = alive

    def is_alive(self):
        return self._alive

    def set_alive(self, new_alive: bool):
        self._alive = new_alive