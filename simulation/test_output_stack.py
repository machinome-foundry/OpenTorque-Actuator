# SPDX-FileCopyrightText: 2026 Luis Henrique Cassis Fagundes
# SPDX-License-Identifier: AGPL-3.0-or-later
# Design: Gabrael Levine (G-Levine); source and modifications in root NOTICE.

"""Mechanical contracts for the source-defined actuator output stack."""

from __future__ import annotations

import hashlib
from pathlib import Path

import numpy as np

from solid_node.test import TestCase

from .layout import SOURCE_Z_BOUNDS, STEP_SHA256
from .output_stack import OutputStackPreview


PROJECT_ROOT = Path(__file__).resolve().parent.parent
PRINTED_PARTS = (
    "actuator_housing",
    "bearing_retainer",
    "planet_carrier_a",
    "planet_carrier_b",
    "planet_carrier_c",
    "backplate",
    "encoder_cover",
    "encoder_magnet_holder",
)
COAXIAL_PARTS = (
    "actuator_housing",
    "planet_carrier_a",
    "planet_carrier_b",
    "planet_carrier_c",
    "backplate",
    "encoder_magnet_holder",
)


def exact_bounds(node):
    """Return the source solid's exact local bounds, independent of STL facets."""

    bounds = node.shape().BoundingBox()
    return np.array(
        (
            (bounds.xmin, bounds.ymin, bounds.zmin),
            (bounds.xmax, bounds.ymax, bounds.zmax),
        )
    )


class OutputStackTest(TestCase):
    node = OutputStackPreview

    @property
    def stack(self):
        return self.node.output_stack

    def test_all_source_prints_are_selected(self):
        for name in PRINTED_PARTS:
            with self.subTest(part=name):
                self.assertTrue(hasattr(self.stack, name), f"missing STEP product: {name}")

    def test_source_axial_bounds_are_preserved(self):
        for name, expected in SOURCE_Z_BOUNDS.items():
            with self.subTest(part=name):
                measured = getattr(self.stack, name).mesh.bounds[:, 2]
                np.testing.assert_allclose(measured, expected, atol=0.01)

    def test_source_axis_is_preserved(self):
        for name in COAXIAL_PARTS:
            with self.subTest(part=name):
                bounds = exact_bounds(getattr(self.stack, name))
                center_xy = (bounds[0, :2] + bounds[1, :2]) / 2
                np.testing.assert_allclose(center_xy, (0.0, 0.0), atol=0.01)

    def test_cross_roller_races_use_the_catalogue_seat(self):
        outer = self.stack.cross_roller_outer.mesh.bounds
        inner = self.stack.cross_roller_inner.mesh.bounds
        np.testing.assert_allclose(outer[:, 2], (62.60, 70.60), atol=0.01)
        np.testing.assert_allclose(inner[:, 2], (62.55, 70.55), atol=0.01)
        self.assertAlmostEqual(float(np.ptp(outer[:, 0])), 95.8, delta=0.01)
        self.assertAlmostEqual(float(np.ptp(inner[:, 0])), 86.8, delta=0.01)
        self.assertNotIntersecting(self.stack.cross_roller_outer, self.stack.cross_roller_inner)

    def test_printed_solids_are_connected(self):
        self.assertNoDisconnectedSolids(self.node)

    def test_assembled_step_fingerprint_is_reviewed(self):
        source = PROJECT_ROOT / "STEP" / "opentorque.step"
        measured = hashlib.sha256(source.read_bytes()).hexdigest()
        self.assertEqual(measured, STEP_SHA256)
