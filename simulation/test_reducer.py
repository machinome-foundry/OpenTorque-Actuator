# SPDX-FileCopyrightText: 2026 Luis Henrique Cassis Fagundes
# SPDX-License-Identifier: AGPL-3.0-or-later
# Design: Gabrael Levine (G-Levine); source and modifications in root NOTICE.

"""Mechanical contracts for the OpenTorque planetary reducer."""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np

from solid_node.test import TestCase

from .kinematics import output_angle, planet_absolute_angle, planet_relative_angle
from .reducer import ReducerPosePreview, ReducerPreview
from .tools.probe import radial_harmonics


PROJECT_ROOT = Path(__file__).resolve().parent.parent
EXPECTED_PLANET_XY = (
    (0.0, 27.0),
    (-23.382685902, -13.5),
    (23.382685902, -13.5),
)


def center_xy(node):
    bounds = node.mesh.bounds
    return (bounds[0, :2] + bounds[1, :2]) / 2


def planet_bore_center_xy(node, expected):
    """Measure the 14 mm planet bore instead of tessellated tooth-tip bounds."""

    vertices = node.mesh.vertices[:, :2]
    expected = np.asarray(expected)
    bore = vertices[np.linalg.norm(vertices - expected, axis=1) < 7.1]
    if len(bore) < 8:
        raise AssertionError(f"planet bore vertices not found near {expected}")
    return bore.mean(axis=0)


class ReducerTest(TestCase):
    node = ReducerPreview

    def test_source_tooth_harmonics(self):
        sun = radial_harmonics(PROJECT_ROOT / "STL" / "Sun Gear.stl", (9, 18))
        planet = radial_harmonics(PROJECT_ROOT / "STL" / "Planet Gear.stl", (27, 54))
        self.assertEqual(sun["strongest_frequencies"][0][0], 9)
        self.assertIn(18, [entry[0] for entry in sun["strongest_frequencies"]])
        self.assertEqual(planet["strongest_frequencies"][0][0], 27)
        self.assertIn(54, [entry[0] for entry in planet["strongest_frequencies"]])

    def test_fixed_ring_planetary_relations(self):
        self.assertAlmostEqual(output_angle(360.0), 45.0, delta=1e-9)
        self.assertAlmostEqual(planet_relative_angle(360.0), -105.0, delta=1e-9)
        self.assertAlmostEqual(planet_absolute_angle(360.0), -60.0, delta=1e-9)
        self.assertAlmostEqual(output_angle(2880.0), 360.0, delta=1e-9)
        self.assertAlmostEqual(planet_absolute_angle(2880.0), -480.0, delta=1e-9)

    def test_three_planet_centers_match_the_step(self):
        for index, expected in enumerate(EXPECTED_PLANET_XY, start=1):
            with self.subTest(planet=index):
                unit = getattr(self.node.reducer, f"planet_{index}")
                np.testing.assert_allclose(
                    planet_bore_center_xy(unit.planet_gear, expected), expected, atol=0.01
                )

    def test_planets_are_120_degrees_apart(self):
        centers = [
            planet_bore_center_xy(
                getattr(self.node.reducer, f"planet_{index}").planet_gear,
                EXPECTED_PLANET_XY[index - 1],
            )
            for index in range(1, 4)
        ]
        phases = [math.degrees(math.atan2(y, x)) for x, y in centers]
        separations = sorted((phases[(i + 1) % 3] - phases[i]) % 360 for i in range(3))
        np.testing.assert_allclose(separations, (120.0, 120.0, 120.0), atol=0.01)

    def test_planet_bearing_and_pin_are_coaxial(self):
        for index in range(1, 4):
            with self.subTest(planet=index):
                unit = getattr(self.node.reducer, f"planet_{index}")
                expected = EXPECTED_PLANET_XY[index - 1]
                np.testing.assert_allclose(
                    planet_bore_center_xy(unit.planet_gear, expected), expected, atol=0.01
                )
                np.testing.assert_allclose(center_xy(unit.bearing), expected, atol=0.01)
                np.testing.assert_allclose(center_xy(unit.pin), expected, atol=0.01)

    def test_planet_centers_follow_carrier_angle(self):
        expected_phase = math.radians(90.0 + 45.0)
        expected = (27.0 * math.cos(expected_phase), 27.0 * math.sin(expected_phase))
        try:
            self.node.set_state(input_angle=360.0)
            first_center = planet_bore_center_xy(
                self.node.reducer.planet_1.planet_gear, expected
            )
            np.testing.assert_allclose(first_center, expected, atol=0.01)
        finally:
            self.node.set_state(input_angle=0.0)

    def test_reducer_solids_are_connected(self):
        self.assertNoDisconnectedSolids(self.node)


class ReducerPosePreviewTest(TestCase):
    node = ReducerPosePreview

    def test_time_one_is_one_motor_turn(self):
        try:
            self.node.set_keyframe(1.0)
            self.assertEqual(self.node.reducer.input_angle.value, 360.0)
        finally:
            self.node.clear_keyframe()
