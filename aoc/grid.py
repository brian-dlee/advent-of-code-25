import typing

Grid = list[str]


def read_grid(lines: typing.TextIO) -> Grid:
    grid: list[str] = []

    for line in lines:
        grid.append(line.strip())

    return grid


def read_point(grid: Grid, x: int, y: int) -> str | None:
    if y < 0 or y >= len(grid):
        return None

    if x < 0 or x >= len(grid[0]):
        return None

    return grid[y][x]


def write_point(grid: Grid, x: int, y: int, value: str):
    grid[y] = grid[y][:x] + value + grid[y][x + 1 :]
