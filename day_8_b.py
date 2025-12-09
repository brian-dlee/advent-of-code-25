import argparse
import coloredlogs
import logging
import math
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

    junction_boxes: list[tuple[int, int, int]] = []

    with pathlib.Path(input_filename).open("r") as fp:
        for line in fp:
            x, y, z = tuple(map(int, line.strip().split(",")))

            junction_boxes.append((x, y, z))

    for x, y, z in junction_boxes:
        logging.debug(f"box {(x, y, z)}")

    distances: list[tuple[int, int, float]] = []

    for i in range(len(junction_boxes)):
        for j in range(i + 1, len(junction_boxes)):
            i, j = sorted([i, j])

            ax, ay, az = junction_boxes[i]
            bx, by, bz = junction_boxes[j]

            distances.append((i, j, math.sqrt(math.pow(bx - ax, 2) + math.pow(by - ay, 2) + math.pow(bz - az, 2))))

    distances.sort(key=lambda values: values[2])

    for a, b, distance in distances:
        logging.debug(f"dis {junction_boxes[a]} to {junction_boxes[b]} (distance: {distance})")

    connections: dict[int, set[int]] = {}

    last_connected_junction_boxes_x: tuple[int, int] = (0, 0)

    while True:
        if len(distances) == 0:
            break

        a_i, b_i, distance = distances.pop(0)

        if a_i in connections and b_i in connections[a_i]:
            continue

        a = junction_boxes[a_i]
        b = junction_boxes[b_i]

        last_connected_junction_boxes_x = (a[0], b[0])

        logging.debug(f"con {junction_boxes[a_i]} to {junction_boxes[b_i]} (distance: {distance})")

        next_circuit = set([a_i, b_i])

        if a_i in connections:
            next_circuit.update(connections[a_i])

        if b_i in connections:
            next_circuit.update(connections[b_i])

        if debug:
            debug_circuit = expand_circuit(next_circuit, junction_boxes)

            logging.debug(f"cir {debug_circuit} (size: {len(debug_circuit)})")

        for i in next_circuit:
            connections[i] = next_circuit

        if len(next_circuit) == len(junction_boxes):
            break

    solution = last_connected_junction_boxes_x[0] * last_connected_junction_boxes_x[1]

    logging.info(f"Solution: {solution}")


def expand_circuit(circuit: set[int], boxes: list[tuple[int, int, int]]):
    result: list[tuple[int, int, int]] = []

    for box in map(lambda i: boxes[i], circuit):
        result.append(box)

    return result


if __name__ == "__main__":
    main()
