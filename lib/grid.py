from collections import abc
import enum
import random
import typing

class Cell(enum.IntEnum):
    FREE = 0
    WALL = 1

class Grid:
    __slots__: tuple[str, ...] = ("cells", "height", "width")

    NEIGHBOUR_OFFSETS: tuple[tuple[int, int], ...] = (
        (-1, 0), (0, -1), (1, 0), (0, 1),
    )

    cells: list[Cell]
    height: int
    width: int

    def __init__(self, cells: list[Cell], height: int, width: int):
        if len(cells) != height * width:
            raise ValueError("len(cells) != height * width")

        self.cells = cells
        self.height = height
        self.width = width

    def __getitem__(self, index: tuple[int, int]) -> Cell:
        x, y = index

        if y >= self.height or x >= self.width:
            raise IndexError("grid index out of range")

        return self.cells[y * self.width + x]

    @classmethod
    def generate(cls, height: int, width: int, root: int, target: int) -> typing.Self:
        length = height * width

        if root >= length:
            raise IndexError("root index out of range")

        if target >= length:
            raise IndexError("target index out of range")

        cells = [Cell.WALL if random.random() < 0.3 else Cell.FREE for _ in range(height * width)]
        cells[root] = Cell.FREE
        cells[target] = Cell.FREE

        return cls(
            cells,
            height,
            width
        )

    def neighbours(self, cell: int) -> abc.Iterator[tuple[int, int]]:
        x, y = cell % self.width, cell // self.width

        for dx, dy in type(self).NEIGHBOUR_OFFSETS:
            nx, ny = x + dx, y + dy

            if 0 <= ny < self.height and 0 <= nx < self.width and self[nx, ny] != Cell.WALL:
                yield nx, ny
