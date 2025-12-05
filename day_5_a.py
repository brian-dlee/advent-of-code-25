import argparse
import coloredlogs
import logging
import pathlib
import typing


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

    ranges: list[tuple[int, int]] = []
    ingredients: list[int] = []

    with pathlib.Path(input_filename).open("r") as fp:
        parse_mode = "ranges"

        for line in fp:
            line = line.strip()

            if line == "":
                parse_mode = "ingredients"
                continue

            if parse_mode == "ranges":
                start, end = map(int, line.split("-"))
                ranges.append((start, end))
            else:
                ingredients.append(int(line))

    for ingredient in ingredients:
        for start, end in ranges:
            if start <= ingredient <= end:
                solution += 1
                break

    logging.info(f"Solution: {solution}")


if __name__ == "__main__":
    main()
