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

    for x in range(len(g[0])):
        if grid.read_point(g, x, 0) == "S":
            start_position = (x, 0)

    assert start_position is not None

    beam_positions: set[tuple[int, int]] = set()

    def count_tachyon_splits(position: tuple[int, int]) -> int:
        next_position = position

        while True:
            if next_position in beam_positions:
                return 0

            logging.debug(f"Position: {next_position}")

            beam_positions.add(next_position)

            if debug:
                display_grid_debug(g, beam_positions)

            match grid.read_point(g, *next_position):
                case None:
                    return 0
                case "^":
                    split_l: tuple[int, int] = next_position[0] - 1, next_position[1]
                    split_count_l = count_tachyon_splits(split_l)

                    split_r: tuple[int, int] = next_position[0] + 1, next_position[1]
                    split_count_r = count_tachyon_splits(split_r)

                    return 1 + split_count_l + split_count_r
                case _:
                    next_position = next_position[0], next_position[1] + 1

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
