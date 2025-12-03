#!/bin/bash

set -e

if [[ $# -lt 1 ]]; then
  echo "No filename provided" >&2
  exit 1
fi

cat >"$1" <<EOF
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
        level=logging.DEBUG if debug else logging.INFO
    )

    logging.info(f"Input file: {input_filename}")

    solution = 0

    with pathlib.Path(input_filename).open("r") as fp:
        for line in fp:
            logging.debug("Reading line: %s", line.strip())

            solution += len(line)

    logging.info(f"Solution: {solution}")


if __name__ == "__main__":
    main()

EOF
