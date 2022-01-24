import random
from abc import ABC, abstractmethod
from typing import List

class StartingPattern(ABC):

    @abstractmethod
    def generate(self) -> set:
        pass

    @staticmethod
    def from_array(array: List[list]) -> set:
        cells = set()
        for r, row in enumerate(reversed(array)):
            for c, cell in enumerate(row):
                if cell:
                    cells.add((c, r))
        return cells


class CustomPattern(StartingPattern):

    def __init__(self, array):
        self.array = array

    def generate(self):
        return self.from_array(self.array)


class Acorn(StartingPattern):
    def __init__(self):
        self.acorn = [
            [0,1,0,0,0,0,0],
            [0,0,0,1,0,0,0],
            [1,1,0,0,1,1,1]
        ]

    def generate(self):
        return self.from_array(self.acorn)


class GliderGun(StartingPattern):
    def __init__(self):
        self.glider = [
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [1,1,0,0,0,0,0,0,0,0,1,0,0,0,1,0,1,1,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        ]

    def generate(self):
        return self.from_array(self.glider)


class RandomPattern(StartingPattern):

    def __init__(self, width: int, height: int, sparsity=6, seed: int=None):
        self.width, self.height = width, height
        self.sparsity = sparsity
        random.seed(seed)

    def generate(self) -> set:
        living_cells = set()
        for x in range(-self.width//2, self.width//2):
            for y in range(-self.height//2, self.height//2):
                if random.randint(0, self.sparsity) == 0:
                    living_cells.add((x, y))
        random.seed(None)
        return living_cells

