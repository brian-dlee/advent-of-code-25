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
    _ = parser.add_argument("--limit", type=int, default=1000)
    args = parser.parse_args()

    input_filename: str = typing.cast(str, args.input_filename)
    debug: bool = typing.cast(bool, args.debug)
    limit: int = typing.cast(int, args.limit)

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

    for i in range(limit):
        if len(distances) == 0:
            break

        a_i, b_i, distance = distances.pop(0)

        if a_i in connections and b_i in connections[a_i]:
            continue

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

    unique_circuits: dict[int, set[int]] = {}

    for circuit in connections.values():
        unique_circuits[id(circuit)] = circuit

    circuits = list(unique_circuits.values())

    for i in range(len(junction_boxes)):
        if i not in connections:
            circuits.append(set([i]))

    circuits.sort(key=lambda boxes: len(boxes), reverse=True)

    logging.debug(f"Displaying circuits")

    for i, circuit in enumerate(circuits):
        logging.debug(f"circuit {i:03d}: (size: {len(circuit)}) {expand_circuit(circuit, junction_boxes)}")

    solution = 1

    for i, circuit in enumerate(circuits[0:3]):
        logging.info(f"Circuit rank {i + 1}: {len(circuit)}")
        solution *= len(circuit)

    logging.info(f"Solution: {solution}")


def expand_circuit(circuit: set[int], boxes: list[tuple[int, int, int]]):
    result: list[tuple[int, int, int]] = []

    for box in map(lambda i: boxes[i], circuit):
        result.append(box)

    return result


if __name__ == "__main__":
    main()
