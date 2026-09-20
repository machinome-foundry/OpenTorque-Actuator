# SPDX-FileCopyrightText: 2026 Luis Henrique Cassis Fagundes
# SPDX-License-Identifier: CC-BY-SA-4.0
# Design: Gabrael Levine (G-Levine); source and modifications in root NOTICE.

"""Planetary reduction stage of the OpenTorque actuator."""

from machinome.node import AssemblyNode
from machinome.motion.joints import Revolute
from machinome.motion.ports import RotationalPort
from machinome.simulation import Driver
from machinome_mechanics import internal_mesh_angle

from .hardware import PlanetBearing
from .kinematics import output_angle
from .layout import (
    CARRIER_RATIO,
    GEAR_GROUP_Z,
    PLANET_BEARING_Z,
    PLANET_GEAR_Z,
    PLANET_PHASES,
    PLANET_RADIUS,
    PLANET_TEETH,
    RING_TEETH,
)
from .parts import PlanetGear, PlanetPin, SunGear


def _fixed_ring_planet_spin(orbit, planet):
    """The fixed-ring mesh expressed in the planet's orbiting frame."""
    return lambda carrier: (
        internal_mesh_angle(0.0, RING_TEETH, PLANET_TEETH, carrier) - carrier
    )


class PlanetUnit(AssemblyNode):
    """One source planet, its connected bearing envelope, and source pin."""

    orbit = Revolute(axis=(0, 0, 1), unit="deg")

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


class PlanetaryReducer(AssemblyNode):
    """Sun and three planets of the fixed-ring 8:1 reducer."""

    sun_gear = SunGear()
    planet_1 = PlanetUnit()
    planet_2 = PlanetUnit()
    planet_3 = PlanetUnit()

    sun_gear.spin.drives(planet_1.orbit, ratio=CARRIER_RATIO)
    sun_gear.spin.drives(planet_2.orbit, ratio=CARRIER_RATIO)
    sun_gear.spin.drives(planet_3.orbit, ratio=CARRIER_RATIO)
    planet_1.orbit.drives(planet_1.planet_gear.spin,
                          law=_fixed_ring_planet_spin)
    planet_2.orbit.drives(planet_2.planet_gear.spin,
                          law=_fixed_ring_planet_spin)
    planet_3.orbit.drives(planet_3.planet_gear.spin,
                          law=_fixed_ring_planet_spin)

    def render(self):
        self.sun_gear.translate((0.0, 0.0, GEAR_GROUP_Z))
        self.planet_2.rotate(PLANET_PHASES[1], (0.0, 0.0, 1.0))
        self.planet_3.rotate(PLANET_PHASES[2], (0.0, 0.0, 1.0))


class ReducerPreview(AssemblyNode):
    """Ground-up reducer preview with a builder-facing input angle."""

    input_angle = Driver(default=0.0, range=(-2880.0, 2880.0), unit="deg")
    reducer = PlanetaryReducer()

    # Named so a subclass may replace it (ADR-099, whole-tree fixpoint).
    drive = input_angle.drives(reducer.sun_gear.spin)

    @property
    def output_angle(self):
        return output_angle(self.input_angle)


class ReducerPosePreview(ReducerPreview):
    """Snapshot-only reducer preview: one motor turn over normalized time.

    A SUBCLASS of `ReducerPreview` rather than a separate ground-up class:
    it inherits `reducer` and REPLACES the base's named `drive` relation,
    at the position the base's held, with one sourced from its own
    time-bound port instead of `input_angle` (ADR-099, whole-tree
    fixpoint: a subclass assigning a relation to a name a base used
    replaces it; a bare statement stays additive).
    """

    free_run = RotationalPort(unit="deg")

    drive = free_run.drives(ReducerPreview.reducer.sun_gear.spin)

    def simulate(self):
        self.free_run = 360.0 * self.time
