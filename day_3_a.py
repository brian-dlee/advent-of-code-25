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

    with pathlib.Path(input_filename).open("r") as fp:
        for line in fp:
            logging.debug("Reading line: %s", line)

            batteries = list(map(int, line.strip()))

            first_battery_power = batteries[0]
            first_battery_index = 0

            for i in range(1, len(batteries) - 1):
                battery = batteries[i]

                if battery > first_battery_power:
                    first_battery_power = battery
                    first_battery_index = i

            logging.debug("First battery: %s (index: %s)", first_battery_power, first_battery_index)

            second_battery_power = batteries[first_battery_index + 1]
            second_battery_index = first_battery_index + 1

            for i in range(second_battery_index, len(batteries)):
                battery = batteries[i]

                if battery > second_battery_power:
                    second_battery_power = battery
                    second_battery_index = i

            logging.debug("Second battery: %s (index: %s)", second_battery_power, second_battery_index)

            battery_power = first_battery_power * 10 + second_battery_power

            logging.debug("Battery: %s", battery_power)

            solution += battery_power

    logging.info(f"Solution: {solution}")


if __name__ == "__main__":
    main()
