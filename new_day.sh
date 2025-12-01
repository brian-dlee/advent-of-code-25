#!/bin/bash

set -e

if [[ $# -lt 1 ]]; then
  echo "No filename provided" >&2
  exit 1
fi

cat >"$1" <<EOF
import argparse
import pathlib
import typing


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_filename")
    args = parser.parse_args()

    input_filename: str = typing.cast(str, args.input_filename)

    print("Input file: {input_filename}")

    solution = 0
    lines: list[str] = []

    with pathlib.Path(input_filename).open("r") as fp:
        for line in fp:
            lines.append(line)

    print(f"Read {len(lines)} lines from {input_filename}")

    # ...

    print(f"Solution: {solution}")


if __name__ == "__main__":
    main()

EOF
