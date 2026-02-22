from slimgui import imgui

from lib.algorithms import Algorithm
from lib.algorithms.astar import AStar
from lib.algorithms.bfs import BFS
from lib.algorithms.bibfs import BiBFS
from lib.grid import Grid


class AlgorithmManager:
    __slots__: tuple[str, ...] = ("algorithm_instance", "algorithm_selection")

    ALGORITHMS: tuple[type[Algorithm], ...] = (
        AStar,
        BFS,
        BiBFS,
    )

    LABELS: tuple[str, ...] = (
        "A*",
        "BFS",
        "Bi-BFS",
    )

    algorithm_instance: Algorithm | None
    algorithm_selection: int

    def __init__(self) -> None:
        self.algorithm_instance = None
        self.algorithm_selection = 0

    def instantiate_algorithm(self, grid: Grid, root: int, target: int):
        self.algorithm_instance = type(self).ALGORITHMS[self.algorithm_selection](
            grid, root, target
        )

    def render(self):
        imgui.push_item_width(-1)
        changed, new_selection = imgui.combo(
            "##algorithm", self.algorithm_selection, type(self).LABELS
        )
        imgui.pop_item_width()

        if changed:
            self.algorithm_selection = new_selection
