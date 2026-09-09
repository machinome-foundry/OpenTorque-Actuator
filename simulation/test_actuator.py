# SPDX-FileCopyrightText: 2026 Luis Henrique Cassis Fagundes
# SPDX-License-Identifier: AGPL-3.0-or-later
# Design: Gabrael Levine (G-Levine); source and modifications in root NOTICE.

"""Whole-machine controls, scenario, and integrity contracts."""

from solid_node.simulation import ScenarioTest, qualified_drivers, qualified_instructions
from solid_node.test import TestCase

from .actuator import ActuatorPosePreview, OpenTorqueActuator
from .seats import assert_seat_inventory


class OpenTorqueActuatorTest(TestCase):
    node = OpenTorqueActuator

    def test_builder_control_surface(self):
        self.assertEqual(list(qualified_drivers(self.node)), ["input_angle"])
        self.assertEqual(
            list(qualified_instructions(self.node)),
            ["Home", "One Motor Turn", "One Output Turn"],
        )

    def test_driver_reaches_every_motion_group(self):
        try:
            self.node.set_state(input_angle=360.0)
            self.assertEqual(self.node.reducer.sun_gear.spin.value, 360.0)
            self.assertEqual(self.node.output_stack.planet_carrier_b.turn.value, 45.0)
        finally:
            self.node.set_state(input_angle=0.0)

    def test_solid_integrity(self):
        self.assertNoDisconnectedSolids(self.node)

    def test_assembly_integrity_at_named_targets(self):
        try:
            for input_angle in (0.0, 360.0, 2880.0):
                with self.subTest(input_angle=input_angle):
                    self.node.set_state(input_angle=input_angle)
                    assert_seat_inventory(self, self.node)
        finally:
            self.node.set_state(input_angle=0.0)


class ActuatorInstructionScenarioTest(ScenarioTest):
    node = OpenTorqueActuator
    dt = 0.5
    meshes = True

    def test_named_moves_land_and_remain_coherent(self):
        sim = self.simulation()
        sim.every(0.5, assert_seat_inventory, self, self.node)

        sim.at(0.0).trigger("One Motor Turn")
        sim.run(1.0)
        self.assertEqual(sim.state["input_angle"], 360.0)

        sim.at(sim.time).trigger("One Output Turn")
        sim.run(8.0)
        self.assertEqual(sim.state["input_angle"], 2880.0)

        sim.at(sim.time).trigger("Home")
        sim.run(8.0)
        self.assertEqual(sim.state["input_angle"], 0.0)


class ActuatorPosePreviewTest(TestCase):
    node = ActuatorPosePreview

    def test_time_one_is_one_motor_turn(self):
        try:
            self.node.set_keyframe(1.0)
            self.assertEqual(self.node.reducer.sun_gear.spin.value, 360.0)
            self.assertEqual(self.node.output_stack.planet_carrier_b.turn.value, 45.0)
        finally:
            self.node.clear_keyframe()
