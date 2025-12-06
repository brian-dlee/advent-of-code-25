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

    problem_count = 0
    digits: list[str] = []

    with pathlib.Path(input_filename).open("r") as fp:
        for line in fp:
            line = line.strip("\n")

            if len(digits) < len(line):
                digits = [""] * len(line)

            for i, char in enumerate(line):
                if char == " ":
                    digits[i] += " "
                else:
                    digits[i] += char

                    if char in ("+", "*"):
                        problem_count += 1

    problems: list[list[int]] = []

    for _ in range(problem_count):
        problems.append([])

    ops: list[str] = [""] * problem_count

    problem_i = 0

    for i, word in enumerate(reversed(digits)):
        # print(f"WORD {i:04d}", ":", f"{word=}")

        if word.isspace():
            # print(f"PROBLEM {problem_i:04d}", ":", problems[problem_i], ops[problem_i])
            problem_i += 1
            continue

        number = int(word[0:-1])
        op_or_zero = word[-1]

        problems[problem_i].append(number)

        if op_or_zero != "0":
            ops[problem_i] = op_or_zero

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
