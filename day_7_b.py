import argparse
import coloredlogs
import logging
import pathlib
import sys
import typing

from aoc import grid


def main():
    parser = argparse.ArgumentParser()
    _ = parser.add_argument("input_filename")
    _ = parser.add_argument("--debug", action="store_true")
    _ = parser.add_argument("--test", action="store_true")
    args = parser.parse_args()

    input_filename: str = typing.cast(str, args.input_filename)
    debug: bool = typing.cast(bool, args.debug)

    coloredlogs.install(
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.DEBUG if debug else logging.INFO,
    )

    logging.info(f"Input file: {input_filename}")

    solution = 0

    with pathlib.Path(input_filename).open("r") as fp:
        g = grid.read_grid(fp)

    start_position: tuple[int, int] | None = None

    assert len(g) > 0, "Grid is empty"

    grid_w = len(g[0])
    grid_h = len(g)

    for x in range(len(g[0])):
        if grid.read_point(g, x, 0) == "S":
            start_position = (x, 0)

    assert start_position is not None, "Start position not found"

    def count_tachyon_splits(position: tuple[int, int]):
        y = 1

        timelines = {position[0]: 1}

        while True:
            if y >= grid_h:
                return sum(count for _, count in timelines.items())

            next_timelines: dict[int, int] = {}

            for x in range(grid_w):
                count = timelines.get(x)

                if count is None:
                    continue

                if grid.read_point(g, x, y) == "^":
                    if x > 0:
                        _ = next_timelines.setdefault(x - 1, 0)
                        next_timelines[x - 1] += count

                    if x < grid_w - 1:
                        _ = next_timelines.setdefault(x + 1, 0)
                        next_timelines[x + 1] += count
                else:
                    _ = next_timelines.setdefault(x, 0)
                    next_timelines[x] += count

            timelines = next_timelines

            y += 1

    solution = count_tachyon_splits(start_position)

    logging.info(f"Solution: {solution}")


def display_grid_debug(g: grid.Grid, beam_positions: set[tuple[int, int]]):
    for y, row in enumerate(g):
        for x, cell in enumerate(row):
            if cell in ("S", "^") or (x, y) not in beam_positions:
                print(cell, file=sys.stderr, end="")
            else:
                print("|", file=sys.stderr, end="")

        print(file=sys.stderr)


if __name__ == "__main__":
    main()
