# SPDX-FileCopyrightText: 2026 Luis Henrique Cassis Fagundes
# SPDX-License-Identifier: CC-BY-SA-4.0
# Design: Gabrael Levine (G-Levine); source and modifications in root NOTICE.

"""Measured source layout and kinematic constants, in millimetres/degrees."""

STEP_SHA256 = "715965dc130555453d7d76d7ab51beeb8a5566a35cc37aae25cbb81151c879a3"
SEAT_WITNESS = 0.05

PLANET_RADIUS = 27.0
PLANET_PHASES = (0.0, 120.0, -120.0)
PLANET_XY = (
    (0.0, 27.0),
    (-23.382685902, -13.5),
    (23.382685902, -13.5),
)
GEAR_GROUP_Z = 40.0
PLANET_GEAR_Z = 1.0
PLANET_BEARING_Z = 10.0

SUN_TEETH = 18
PLANET_TEETH = 54
RING_TEETH = SUN_TEETH + 2 * PLANET_TEETH
REDUCTION = 1.0 + RING_TEETH / SUN_TEETH
CARRIER_RATIO = 1.0 / REDUCTION
SUN_PLANET_MESH = -SUN_TEETH / PLANET_TEETH

SOURCE_Z_BOUNDS = {
    "encoder_cover": (-21.0 - 2 * SEAT_WITNESS, -11.0 - 2 * SEAT_WITNESS),
    "encoder_magnet_holder": (-14.0, -9.0),
    "backplate": (-11.0 - SEAT_WITNESS, -3.5 - SEAT_WITNESS),
    "actuator_housing": (-3.5, 62.5),
    "planet_carrier_c": (36.0 - SEAT_WITNESS, 47.5 - SEAT_WITNESS),
    "planet_carrier_b": (40.0, 62.5),
    "planet_carrier_a": (62.5 + 3 * SEAT_WITNESS, 74.0 + 3 * SEAT_WITNESS),
    "bearing_retainer": (62.5 + SEAT_WITNESS, 73.0 + SEAT_WITNESS),
}
