# SPDX-FileCopyrightText: 2026 Luis Henrique Cassis Fagundes
# SPDX-License-Identifier: CC-BY-SA-4.0
# Design: Gabrael Levine (G-Levine); source and modifications in root NOTICE.

"""Planetary reduction stage of the OpenTorque actuator."""

from solid_node.node import AssemblyNode
from solid_node.motion.ports import RotationalPort
from solid_node.simulation import Driver

from .hardware import PlanetBearing
from .kinematics import output_angle, planet_relative_angle
from .layout import (
    GEAR_GROUP_Z,
    PLANET_BEARING_Z,
    PLANET_GEAR_Z,
    PLANET_PHASES,
    PLANET_RADIUS,
)
from .parts import PlanetGear, PlanetPin, SunGear


class PlanetUnit(AssemblyNode):
    """One source planet, its connected bearing envelope, and source pin."""

    spin = RotationalPort(unit="deg")
    planet_gear = PlanetGear()
    bearing = PlanetBearing()
    pin = PlanetPin()

    def render(self):
        self.planet_gear.translate(
            (0.0, PLANET_RADIUS, GEAR_GROUP_Z + PLANET_GEAR_Z)
        )
        self.bearing.translate(
            (0.0, PLANET_RADIUS, GEAR_GROUP_Z + PLANET_BEARING_Z)
        )
        # The STEP pin product is modelled in context at Y=27 and Z=-3..27.
        self.pin.translate((0.0, 0.0, GEAR_GROUP_Z))

    def simulate(self):
        spin = self.spin.value
        if spin is None:
            raise ValueError("PlanetUnit.spin must be bound by its parent")
        self.planet_gear.rotate(spin, (0.0, 0.0, 1.0))


class PlanetaryReducer(AssemblyNode):
    """Sun and three planets of the fixed-ring 8:1 reducer."""

    input_angle = RotationalPort(unit="deg")
    sun_gear = SunGear()
    planet_1 = PlanetUnit()
    planet_2 = PlanetUnit()
    planet_3 = PlanetUnit()

    def render(self):
        self.sun_gear.translate((0.0, 0.0, GEAR_GROUP_Z))
        self.planet_2.rotate(PLANET_PHASES[1], (0.0, 0.0, 1.0))
        self.planet_3.rotate(PLANET_PHASES[2], (0.0, 0.0, 1.0))

    def simulate(self):
        angle = self.input_angle.value
        if angle is None:
            raise ValueError("PlanetaryReducer.input_angle must be bound by its parent")
        self.sun_gear.rotate(angle, (0.0, 0.0, 1.0))
        carrier_angle = output_angle(angle)
        spin = planet_relative_angle(angle)
        for planet in (self.planet_1, self.planet_2, self.planet_3):
            self.connect(spin, planet.spin)
            planet.rotate(carrier_angle, (0.0, 0.0, 1.0))


class ReducerPreview(AssemblyNode):
    """Ground-up reducer preview with a builder-facing input angle."""

    input_angle = Driver(default=0.0, range=(-2880.0, 2880.0), unit="deg")
    reducer = PlanetaryReducer()

    def simulate(self):
        self.connect(self.input_angle, self.reducer.input_angle)

    @property
    def output_angle(self):
        return output_angle(self.input_angle)


class ReducerPosePreview(AssemblyNode):
    """Snapshot-only reducer preview: one motor turn over normalized time."""

    reducer = PlanetaryReducer()

    def simulate(self):
        self.connect(360.0 * self.time, self.reducer.input_angle)
