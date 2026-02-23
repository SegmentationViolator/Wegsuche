from collections import abc
import enum
import typing

import numpy as np
import numpy.typing as npt


class Cell(enum.IntEnum):
    FREE = 0
    WALL = 1


class Grid:
    __slots__: tuple[str, ...] = ("cells", "height", "width")

    NEIGHBOUR_OFFSETS: npt.NDArray[np.intp] = np.array(
        [
            (-1, 0),
            (0, -1),
            (1, 0),
            (0, 1),
        ],
        dtype=np.intp,
    )

    cells: npt.NDArray[np.int8]
    height: int
    width: int

    def __init__(self, cells: npt.NDArray[np.int8]):
        if cells.ndim != 2:
            raise ValueError("cells must be a 2D array")

        self.cells = cells
        self.height, self.width = cells.shape

    @classmethod
    def generate(
        cls,
        height: int,
        width: int,
        origin: int,
        target: int,
        rng: np.random.Generator,
    ) -> typing.Self:
        length = height * width

        if origin >= length or target >= length:
            raise IndexError("origin or target index out of range")

        cells = rng.random((height, width)) < 0.3
        cells = cells.astype(np.int8) * Cell.WALL

        oy, ox = divmod(origin, width)
        ty, tx = divmod(target, width)

        cells[oy, ox] = Cell.FREE
        cells[ty, tx] = Cell.FREE

        return cls(cells)

    def neighbours(self, cell: int) -> abc.Iterator[int]:
        y, x = divmod(cell, self.width)

        offsets = self.NEIGHBOUR_OFFSETS
        xs = x + offsets[:, 0]
        ys = y + offsets[:, 1]

        in_bounds = (0 <= xs) & (xs < self.width) & (0 <= ys) & (ys < self.height)

        xs = xs[in_bounds]
        ys = ys[in_bounds]

        not_wall = self.cells[ys, xs] != Cell.WALL

        xs = xs[not_wall]
        ys = ys[not_wall]

        for nx, ny in zip(xs, ys):
            yield int(ny) * self.width + int(nx)
