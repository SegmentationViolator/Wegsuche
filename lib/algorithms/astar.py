import heapq
import typing

from lib.grid import Grid

from . import Algorithm

class AStar(Algorithm):
    __slots__: tuple[str, ...] = ("distance", "queue")

    distance: list[int]
    queue: list[tuple[int, int]]

    def __init__(self, grid: Grid, root: int, target: int):
        super().__init__(grid, root, target)

        self.distance = [-1 for _ in range(grid.height * grid.width)]
        self.distance[self.root] = 0
        self.queue = [(self.heuristic(self.root), self.root)]

    def heuristic(self, index: int) -> int:
        x, y = index % self.grid.width, index // self.grid.width
        tx, ty = self.target % self.grid.width, self.target // self.grid.width

        return abs(x - tx) + abs(y - ty)

    @typing.override
    def step(self) -> bool | None:
        if len(self.queue) == 0:
            return False

        _, cell = heapq.heappop(self.queue)

        if cell == self.target:
            return True

        for neighbour in self.grid.neighbours(cell):
            index = neighbour[1] * self.grid.width + neighbour[0]

            if self.distance[index] > -1:
                continue

            self.distance[index] = self.distance[cell] + 1
            self.parent[index] = cell
            score = self.distance[index] + self.heuristic(index)

            heapq.heappush(self.queue, (score, index))

        return None
