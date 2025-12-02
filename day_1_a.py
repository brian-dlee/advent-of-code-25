import argparse
import pathlib
import typing


def main():
    parser = argparse.ArgumentParser()
    _ = parser.add_argument("input_filename")
    args = parser.parse_args()

    input_filename: str = typing.cast(str, args.input_filename)

    print(f"Input file: {input_filename}")

    solution = 0
    current_position = 50

    with pathlib.Path(input_filename).open("r") as fp:
        for line in fp:
            if line.startswith("L"):
                current_position -= int(line[1:])
            else:
                current_position += int(line[1:])

            current_position %= 100

            if current_position == 0:
                solution += 1

    print(f"Solution: {solution}")


if __name__ == "__main__":
    main()
