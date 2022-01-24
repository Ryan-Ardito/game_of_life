from collections import defaultdict
from typing import List

from patterns import StartingPattern


LIVE_RULES  = {2, 3}
SPAWN_RULES = {3}
OFFSETS = (
    (-1, 1), (0, 1), (1, 1),
    (-1, 0),         (1, 0),
    (-1,-1), (0,-1), (1,-1)
)


class GameOfLife:

    def __init__(self, pattern: StartingPattern = None):
        self.living_cells = set()
        if pattern:
            self.living_cells = pattern.generate()

    def evolve(self) -> None:
        """Update the game to the next state"""
        hopefuls = defaultdict(int)
        prev_state: set = self.living_cells.copy()

        for cell in prev_state:
            x, y = cell
            neighbors_alive = 0
            for offset in OFFSETS:
                a, b = offset
                poss = (x + a, y + b)
                if poss in prev_state:
                    neighbors_alive += 1
                else:
                    hopefuls[poss] += 1
            if neighbors_alive not in LIVE_RULES:
                self.living_cells.remove(cell)

        for cell in hopefuls:
            if hopefuls[cell] in SPAWN_RULES:
                self.living_cells.add(cell)

    def bounded_set(self, width: int, height: int) -> set:
        """Generate a set of live cells within a window and adjust coordinates"""
        grid_window = set()
        a, b = width//2, height//2
        for cell in self.living_cells:
            x, y = cell
            cell = (x+a, b+y)
            if cell[1] < 0 or cell[1] > height:
                continue
            elif cell[0] < 0 or cell[0] > width:
                continue
            grid_window.add(cell)
        return grid_window

    def array(self, width: int, height: int) -> List[list]:
        """Generate a 1/0 2d array centered on coordinates (0, 0)"""
        array = []
        for y in range(-height//2, height//2):
            row = []
            for x in range(-width//2, width//2):
                if (x, y) in self.living_cells:
                    row.append(1)
                else:
                    row.append(0)
            array.append(row)
        return array

