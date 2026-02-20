from lib.algorithms.bfs import BFS
from lib.grid import Grid

if __name__ == "__main__":
    H = 9
    W = 16

    root = 0
    target = H * W - 1

    grid = Grid.generate(H, W, root, target)
    path_finder = BFS(grid, root, target)

    for y in range(H):
        row = grid.cells[y*W:(y+1)*W]
        print(" ".join(f"{cell}" for cell in row))

    print()

    found = path_finder.step()
    while found is None:
        found = path_finder.step()

    if not found:
        print("No solution")
        exit()

    path: set[tuple[int, int]] = set()
    current = target
    while current != None:
        x, y = current % W, current // W
        path.add((x, y))
        current = path_finder.parent[current]

    for y in range(H):
        for x in range(W):
            cell = grid[x, y]
            print(f"{'P' if (x, y) in path else cell}", end=' ')
        print()
