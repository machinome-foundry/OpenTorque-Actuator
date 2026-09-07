# SPDX-FileCopyrightText: 2026 Luis Henrique Cassis Fagundes
# SPDX-License-Identifier: CC-BY-SA-4.0
# Design: Gabrael Levine (G-Levine); source and modifications in root NOTICE.

"""Ground-up output stack for the OpenTorque actuator."""

from solid_node.node import AssemblyNode, RotationalPort

from .hardware import CrossRollerInnerRace, CrossRollerOuterRace
from .layout import SEAT_WITNESS
from .parts import (
    ActuatorHousing,
    Backplate,
    BearingRetainer,
    EncoderCover,
    EncoderMagnetHolder,
    PlanetCarrierA,
    PlanetCarrierB,
    PlanetCarrierC,
)


class OutputStack(AssemblyNode):
    """Source-defined shell, carrier, output bearing and encoder-side prints."""

    output_angle = RotationalPort(unit="deg")

    actuator_housing = ActuatorHousing()
    bearing_retainer = BearingRetainer()
    planet_carrier_a = PlanetCarrierA()
    planet_carrier_b = PlanetCarrierB()
    planet_carrier_c = PlanetCarrierC()
    backplate = Backplate()
    encoder_cover = EncoderCover()
    encoder_magnet_holder = EncoderMagnetHolder()
    cross_roller_outer = CrossRollerOuterRace()
    cross_roller_inner = CrossRollerInnerRace()

    def render(self):
        # Witness gaps make source-coincident seats decidable on both kernels.
        self.bearing_retainer.translate((0.0, 0.0, SEAT_WITNESS))
        self.planet_carrier_a.translate((0.0, 0.0, 3 * SEAT_WITNESS))
        self.planet_carrier_c.translate((0.0, 0.0, -SEAT_WITNESS))
        self.backplate.translate((0.0, 0.0, -SEAT_WITNESS))
        self.encoder_cover.translate((0.0, 0.0, -2 * SEAT_WITNESS))
        self.cross_roller_outer.translate((0.0, 0.0, 62.5 + 2 * SEAT_WITNESS))
        self.cross_roller_inner.translate((0.0, 0.0, 62.5 + SEAT_WITNESS))

    def simulate(self):
        angle = self.output_angle.value
        if angle is None:
            raise ValueError("OutputStack.output_angle must be bound by its parent")
        self.planet_carrier_a.rotate(angle, (0.0, 0.0, 1.0))
        self.planet_carrier_b.rotate(angle, (0.0, 0.0, 1.0))
        self.planet_carrier_c.rotate(angle, (0.0, 0.0, 1.0))
        self.encoder_magnet_holder.rotate(angle, (0.0, 0.0, 1.0))
        self.cross_roller_inner.rotate(angle, (0.0, 0.0, 1.0))


class OutputStackPreview(AssemblyNode):
    """Ground-up preview binding the output stack at its source home pose."""

    output_stack = OutputStack()

    def simulate(self):
        self.connect(0.0, self.output_stack.output_angle)
