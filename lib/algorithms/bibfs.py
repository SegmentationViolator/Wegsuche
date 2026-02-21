import collections
import enum
import typing

from lib.grid import Grid

from . import Algorithm

class Turn(enum.IntEnum):
    Root = enum.auto()
    Target = enum.auto()

class BiBFS(Algorithm):
    __slots__: tuple[str, ...] = ("queue", "visited")

    queue: collections.deque[tuple[int, Turn]]
    visited: list[tuple[bool, Turn | None]]

    def __init__(self, grid: Grid, root: int, target: int):
        super().__init__(grid, root, target)

        self.queue = collections.deque(((self.root, Turn.Root), (self.target, Turn.Target)))
        self.visited = [(False, None) for _ in range(grid.height * grid.width)]
        self.visited[self.root] = (True, Turn.Root)
        self.visited[self.target] = (True, Turn.Target)

    @typing.override
    def step(self) -> bool | None:
        if len(self.queue) == 0:
            return False

        cell, turn = self.queue.popleft()

        for neighbour in self.grid.neighbours(cell):
            index = neighbour[1] * self.grid.width + neighbour[0]

            if self.visited[index][0]:
                if self.visited[index][1] != turn:
                    match turn:
                        case Turn.Root:
                            previous = cell
                            current = index
                            next = self.parent[current]
                        case Turn.Target:
                            previous = index
                            current = cell
                            next = self.parent[current]

                    while current is not None:
                        self.parent[current] = previous
                        previous = current
                        current = next

                        if next is not None:
                            next = self.parent[next]

                    print(1)
                    return True
                continue

            self.queue.append((index, turn))
            self.parent[index] = cell
            self.visited[index] = (True, turn)

        return None
