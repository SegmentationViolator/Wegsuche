from lib.algorithms import Algorithm
from lib.algorithms.astar import AStar
from lib.algorithms.bfs import BFS
from lib.algorithms.bibfs import BiBFS
from lib.grid import Grid

if __name__ == "__main__":
    def main():
        H = 9
        W = 16

        root = 0
        target = H * W - 1

        grid = Grid.generate(H, W, root, target)
        path_finder: Algorithm = BiBFS(grid, root, target)

        for y in range(H):
            row = grid.cells[y*W:(y+1)*W]
            print(" ".join(f"{cell}" for cell in row))

        print()

        found = path_finder.step()
        while found is None:
            found = path_finder.step()

        if not found:
            return print("No solution")

        path: set[int] = set()
        current = target
        while current != None:
            path.add(current)
            current = path_finder.parent[current]

        for y in range(H):
            for x in range(W):
                cell = grid[x, y]
                print(f"{'P' if y * W + x in path else cell}", end=' ')
            print()

    main()
