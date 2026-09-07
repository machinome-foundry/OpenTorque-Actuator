# SPDX-FileCopyrightText: 2026 Luis Henrique Cassis Fagundes
# SPDX-License-Identifier: CC-BY-SA-4.0
# Design: Gabrael Levine (G-Levine); source and modifications in root NOTICE.

"""Explicit inventory of source-defined rigid overlaps.

The upstream assembly contains meshing teeth and captured bearing seats, so the
whole-machine contract compares the complete intersecting pair set and measured
volumes. A new, removed, or materially changed overlap fails.
"""

from __future__ import annotations

from itertools import combinations
import re


VOLUME_PATTERN = re.compile(r"intersection volume ([^)]+)\)")

# Explicit per-pair bounds span the measured faceted and exact-kernel readings.
# They are intentionally local rather than a global intersection epsilon: a pair
# disappearing, appearing, or moving beyond its reviewed source-seat range fails.
EXPECTED_SEATS: dict[tuple[str, str], tuple[float, float]] = {
    ("output_stack.actuator_housing", "reducer.planet_1.planet_gear"): (1.0, 30.0),
    ("output_stack.actuator_housing", "reducer.planet_2.planet_gear"): (1.0, 30.0),
    ("output_stack.actuator_housing", "reducer.planet_3.planet_gear"): (1.0, 30.0),
    ("output_stack.bearing_retainer", "output_stack.cross_roller_outer"): (30.0, 45.0),
    ("output_stack.planet_carrier_b", "reducer.planet_1.bearing"): (180.0, 210.0),
    ("output_stack.planet_carrier_b", "reducer.planet_2.bearing"): (180.0, 210.0),
    ("output_stack.planet_carrier_b", "reducer.planet_3.bearing"): (180.0, 210.0),
    ("output_stack.planet_carrier_c", "reducer.planet_1.bearing"): (180.0, 205.0),
    ("output_stack.planet_carrier_c", "reducer.planet_2.bearing"): (180.0, 205.0),
    ("output_stack.planet_carrier_c", "reducer.planet_3.bearing"): (180.0, 205.0),
    ("reducer.planet_1.bearing", "reducer.planet_1.planet_gear"): (210.0, 245.0),
    ("reducer.planet_1.planet_gear", "reducer.sun_gear"): (1.0, 15.0),
    ("reducer.planet_2.bearing", "reducer.planet_2.planet_gear"): (210.0, 245.0),
    ("reducer.planet_2.planet_gear", "reducer.sun_gear"): (1.0, 15.0),
    ("reducer.planet_3.bearing", "reducer.planet_3.planet_gear"): (210.0, 245.0),
    ("reducer.planet_3.planet_gear", "reducer.sun_gear"): (1.0, 15.0),
}


def rigid_parts(node, prefix=""):
    """Yield qualified paths and topmost rigid nodes below an assembly."""

    for child in node.children:
        path = f"{prefix}.{child.name}" if prefix else child.name
        if child.rigid:
            yield path, child
        else:
            yield from rigid_parts(child, path)


def measured_intersections(test_case, root):
    """Return every pair the framework's selected kernel finds intersecting."""

    intersections = {}
    for (left_name, left), (right_name, right) in combinations(rigid_parts(root), 2):
        try:
            test_case.assertNotIntersecting(left, right)
        except AssertionError as error:
            match = VOLUME_PATTERN.search(str(error))
            if match is None:
                raise
            key = tuple(sorted((left_name, right_name)))
            intersections[key] = float(match.group(1))
    return intersections


def assert_seat_inventory(test_case, root):
    """Require the exact pair set and a bounded volume for every source seat."""

    measured = measured_intersections(test_case, root)
    test_case.assertEqual(
        set(measured),
        set(EXPECTED_SEATS),
        f"rigid intersection inventory changed; measured={measured}",
    )
    for pair, (minimum, maximum) in EXPECTED_SEATS.items():
        test_case.assertGreaterEqual(
            measured[pair], minimum, f"intersection volume shrank for {pair}"
        )
        test_case.assertLessEqual(
            measured[pair], maximum, f"intersection volume grew for {pair}"
        )
