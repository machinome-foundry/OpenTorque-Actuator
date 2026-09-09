# SPDX-FileCopyrightText: 2026 Luis Henrique Cassis Fagundes
# SPDX-License-Identifier: CC-BY-SA-4.0
# Design: Gabrael Levine (G-Levine); source and modifications in root NOTICE.

"""Ground-up output stack for the OpenTorque actuator."""

from solid_node.node import AssemblyNode

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

    # planet_carrier_b is the one rigid output body, printed and bought in
    # five pieces; the other four turn with it.
    planet_carrier_b.turn.drives(planet_carrier_a.turn)
    planet_carrier_b.turn.drives(planet_carrier_c.turn)
    planet_carrier_b.turn.drives(encoder_magnet_holder.turn)
    planet_carrier_b.turn.drives(cross_roller_inner.turn)

    def render(self):
        # Witness gaps make source-coincident seats decidable on both kernels.
        self.bearing_retainer.translate((0.0, 0.0, SEAT_WITNESS))
        self.planet_carrier_a.translate((0.0, 0.0, 3 * SEAT_WITNESS))
        self.planet_carrier_c.translate((0.0, 0.0, -SEAT_WITNESS))
        self.backplate.translate((0.0, 0.0, -SEAT_WITNESS))
        self.encoder_cover.translate((0.0, 0.0, -2 * SEAT_WITNESS))
        self.cross_roller_outer.translate((0.0, 0.0, 62.5 + 2 * SEAT_WITNESS))
        self.cross_roller_inner.translate((0.0, 0.0, 62.5 + SEAT_WITNESS))


class OutputStackPreview(AssemblyNode):
    """Ground-up preview binding the output stack at its source home pose."""

    output_stack = OutputStack()

    def simulate(self):
        self.output_stack.planet_carrier_b.turn = 0.0
