import abc

import numpy as np
import numpy.typing as npt

from lib.grid import Grid


class Algorithm(abc.ABC):
    __slots__: tuple[str, ...] = ("grid", "parent", "path", "root", "target")

    grid: Grid
    parent: npt.NDArray[np.intp]
    path: npt.NDArray[np.intp] | None
    root: int
    target: int

    def __init__(self, grid: Grid, root: int, target: int):
        length = grid.height * grid.width

        if root >= length:
            raise IndexError("root index out of range")

        if target >= length:
            raise IndexError("target index out of range")

        self.grid = grid
        self.parent = np.full(self.grid.height * self.grid.width, -1, dtype=np.intp)
        self.path = None
        self.root = root
        self.target = target

    def construct_path(self):
        path: list[int] = []
        node = self.target

        while self.parent[node] != -1:
            path.append(node)
            node = int(self.parent[node])

        path.append(node)
        path.reverse()

        self.path = np.array(path, dtype=np.intp)

    @abc.abstractmethod
    def explored(self) -> npt.NDArray[np.intp]: ...

    @abc.abstractmethod
    def frontier(self) -> npt.NDArray[np.intp]: ...

    @abc.abstractmethod
    def step(self) -> bool | None: ...
