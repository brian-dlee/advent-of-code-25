import argparse
import coloredlogs
import logging
import pathlib
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

        roll_locations: dict[tuple[int, int], bool] = {}

        for y, row in enumerate(g):
            for x, cell in enumerate(row):
                if cell == "@":
                    roll_locations[(x, y)] = True

        for roll_x, roll_y in roll_locations:
            adjacent = 0

            for t_x in (-1, 0, 1):
                for t_y in (-1, 0, 1):
                    if t_x == 0 and t_y == 0:
                        continue

                    if grid.read_point(g, roll_x + t_x, roll_y + t_y) == "@":
                        adjacent += 1

            if adjacent < 4:
                solution += 1

    logging.info(f"Solution: {solution}")


if __name__ == "__main__":
    main()
