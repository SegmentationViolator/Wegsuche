import collections
import typing

from lib.grid import Grid

from . import Algorithm

class BFS(Algorithm):
    __slots__: tuple[str, ...] = ("parent", "queue", "visited")

    parent: list[int | None]
    queue: collections.deque[int]
    visited: list[bool]

    def __init__(self, grid: Grid, root: int, target: int):
        super().__init__(grid, root, target)

        self.parent = [None for _ in range(grid.height * grid.width)]
        self.queue = collections.deque((self.root,))
        self.visited = [True if i == self.root else False for i in range(grid.height * grid.width)]

    @typing.override
    def step(self) -> bool | None:
        if len(self.queue) == 0:
            return False

        cell = self.queue.popleft()

        if cell == self.target:
            return True

        for neighbour in self.grid.neighbours(cell):
            index = neighbour[1] * self.grid.width + neighbour[0]

            if self.visited[index]:
                continue
            self.queue.append(index)

            self.parent[index] = cell
            self.visited[index] = True

        return None
