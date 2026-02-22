import collections
import typing

import numpy as np
import numpy.typing as npt

from lib.grid import Grid

from . import Algorithm


class BFS(Algorithm):
    __slots__: tuple[str, ...] = ("queue", "_visited")

    queue: collections.deque[int]
    _visited: npt.NDArray[np.bool_]

    def __init__(self, grid: Grid, root: int, target: int):
        super().__init__(grid, root, target)

        self.queue = collections.deque((self.root,))
        self._visited = np.full(grid.height * grid.width, False, dtype=np.bool_)
        self._visited[self.root] = True

    @typing.override
    def explored(self) -> npt.NDArray[np.intp]:
        return np.flatnonzero(self._visited == True)

    @typing.override
    def frontier(self) -> npt.NDArray[np.intp]:
        return np.fromiter(self.queue, dtype=np.intp)

    @typing.override
    def step(self) -> bool | None:
        if len(self.queue) == 0:
            return False

        cell = self.queue.popleft()

        if cell == self.target:
            return True

        for neighbour in self.grid.neighbours(cell):
            if self._visited[neighbour]:
                continue

            self.queue.append(neighbour)
            self.parent[neighbour] = cell
            self._visited[neighbour] = True

        return None
