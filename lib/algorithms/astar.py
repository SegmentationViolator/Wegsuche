import heapq
import typing

import numpy as np
import numpy.typing as npt

from lib.grid import Grid

from . import Algorithm


class AStar(Algorithm):
    __slots__: tuple[str, ...] = ("distance", "queue")

    distance: npt.NDArray[np.int16]
    queue: list[tuple[int, int]]

    def __init__(self, grid: Grid, origin: int, target: int):
        super().__init__(grid, origin, target)

        self.distance = np.full(grid.height * grid.width, -1, dtype=np.int16)
        self.distance[self.origin] = 0
        self.queue = [(self.heuristic(self.origin), self.origin)]

    def heuristic(self, index: int) -> int:
        y, x = divmod(index, self.grid.width)
        ty, tx = divmod(self.target, self.grid.width)

        return abs(x - tx) + abs(y - ty)

    @typing.override
    def explored(self) -> npt.NDArray[np.intp]:
        return np.flatnonzero(self.distance > -1)

    @typing.override
    def frontier(self) -> npt.NDArray[np.intp]:
        return np.fromiter((idx for _, idx in self.queue), dtype=np.intp)

    @typing.override
    def step(self) -> bool | None:
        if len(self.queue) == 0:
            return False

        _, cell = heapq.heappop(self.queue)

        if cell == self.target:
            return True

        for neighbour in self.grid.neighbours(cell):
            if self.distance[neighbour] > -1:
                continue

            self.distance[neighbour] = self.distance[cell] + 1
            self.parent[neighbour] = cell
            score = int(self.distance[neighbour]) + self.heuristic(neighbour)

            heapq.heappush(self.queue, (score, neighbour))

        return None
