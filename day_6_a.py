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

    problems: list[list[int]] = []
    ops: list[str] = []

    with pathlib.Path(input_filename).open("r") as fp:
        for line in fp:
            line = line.strip()

            words = line.split()

            if len(problems) == 0:
                for _ in words:
                    problems.append([])

            if words[0] in ("*", "+"):
                ops = words
            else:
                for i, number in enumerate(map(int, words)):
                    problems[i].append(number)

    for i, problem in enumerate(problems):
        op = ops[i]

        if op == "+":
            solution += sum(problem)
        else:
            answer = 1

            for number in problem:
                answer *= number

            solution += answer

    logging.info(f"Solution: {solution}")


if __name__ == "__main__":
    main()
