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
            logging.debug("Reading line: %s", line.strip())

            batteries = list(map(int, line.strip()))

            selected_battery_p = [0] * 12
            selected_battery_i = [0] * 12

            l_bound = 0
            r_bound = len(batteries) - 11

            for battery_i in range(12):
                selected_battery_p[battery_i] = batteries[l_bound]
                selected_battery_i[battery_i] = l_bound

                logging.debug(
                    "Starting battery %s at %s (index: %s)",
                    battery_i,
                    selected_battery_p[battery_i],
                    selected_battery_i[battery_i],
                )

                logging.debug("Candidates %s [%s-%s]", batteries[l_bound + 1 : r_bound], l_bound + 1, r_bound)

                for i in range(l_bound + 1, r_bound):
                    battery = batteries[i]

                    logging.debug(
                        "Comparing new battery %s (index: %s) to current %s (index: %s)",
                        battery,
                        i,
                        selected_battery_p[battery_i],
                        selected_battery_i[battery_i],
                    )

                    if battery > selected_battery_p[battery_i]:
                        selected_battery_p[battery_i] = battery
                        selected_battery_i[battery_i] = i

                        logging.debug("Updated selected battery %s to %s (index: %s)", battery_i, battery, i)

                        l_bound = i + 1

                l_bound = selected_battery_i[battery_i] + 1
                r_bound += 1

                logging.debug(
                    "Battery %d: %s (index: %s)",
                    battery_i,
                    selected_battery_p[battery_i],
                    selected_battery_i[battery_i],
                )

            battery_power = int("".join(map(str, selected_battery_p)))

            logging.debug("Battery: %s", battery_power)

            solution += battery_power

    logging.info(f"Solution: {solution}")


if __name__ == "__main__":
    main()
