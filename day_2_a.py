import argparse
import collections.abc
import coloredlogs
import logging
import pathlib
import typing


def iter_number_ranges(content: str) -> collections.abc.Iterable[tuple[int, int]]:
    for part in content.split(","):
        start, end = part.split("-")

        yield int(start), int(end)


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
        for start, end in iter_number_ranges(fp.read()):
            logging.debug("Next number range: %s-%s", start, end)

            for n in range(start, end + 1):
                value = str(n)
                value_length = len(value)

                if value_length % 2 != 0:
                    continue

                middle = int(value_length / 2)

                if value[0:middle] == value[middle:]:
                    solution += n

    logging.info(f"Solution: {solution}")


if __name__ == "__main__":
    main()
