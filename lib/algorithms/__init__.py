import abc

from lib.grid import Grid

class Algorithm(abc.ABC):
    __slots__: tuple[str, ...] = ("grid", "root", "target")

    grid: Grid
    root: int
    target: int

    def __init__(self, grid: Grid, root: int, target: int):
        if root >= len(grid.cells):
            raise IndexError("root index out of range")

        if target >= len(grid.cells):
            raise IndexError("target index out of range")

        self.grid = grid
        self.root = root
        self.target = target

    @abc.abstractmethod
    def step(self) -> bool | None:
        ...
