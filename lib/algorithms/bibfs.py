import collections
import enum
import typing

import numpy as np
import numpy.typing as npt

from lib.grid import Grid

from . import Algorithm


class Turn(enum.IntEnum):
    Neither = -1
    Root = 0
    Target = 1


class BiBFS(Algorithm):
    __slots__: tuple[str, ...] = ("frontier_count", "queue", "_visited")

    frontier_count: list[int]
    queue: collections.deque[tuple[int, Turn]]
    _visited: npt.NDArray[np.int8]

    def __init__(self, grid: Grid, root: int, target: int):
        super().__init__(grid, root, target)

        self.frontier_count = [1, 1]
        self.queue = collections.deque(
            ((self.root, Turn.Root), (self.target, Turn.Target))
        )
        self._visited = np.full(grid.height * grid.width, Turn.Neither, dtype=np.int8)
        self._visited[self.root] = Turn.Root
        self._visited[self.target] = Turn.Target

    @typing.override
    def explored(self) -> npt.NDArray[np.intp]:
        return np.flatnonzero(self._visited != Turn.Neither)

    @typing.override
    def frontier(self) -> npt.NDArray[np.intp]:
        return np.fromiter((idx for idx, _ in self.queue), dtype=np.intp)

    @typing.override
    def step(self) -> bool | None:
        if len(self.queue) == 0 or any(map(lambda count: count == 0, self.frontier_count)):
            return False

        cell, turn = self.queue.popleft()
        self.frontier_count[turn] -= 1

        for neighbour in self.grid.neighbours(cell):
            visited = Turn(self._visited[neighbour])

            if visited == turn:
                continue

            if visited != Turn.Neither and visited != turn:
                match turn:
                    case Turn.Root:
                        previous = cell
                        current = neighbour
                    case Turn.Target:
                        previous = neighbour
                        current = cell
                    case Turn.Neither:
                        raise RuntimeError("reached unreachable case")
                next = int(self.parent[current])

                while current > -1:
                    self.parent[current] = previous
                    previous = current
                    current = next

                    if next > -1:
                        next = int(self.parent[next])

                return True

            self.queue.append((neighbour, turn))
            self.frontier_count[turn] += 1
            self.parent[neighbour] = cell
            self._visited[neighbour] = turn

        return None
