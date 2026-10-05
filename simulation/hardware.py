# SPDX-FileCopyrightText: 2026 Luis Henrique Cassis Fagundes
# SPDX-License-Identifier: CC-BY-SA-4.0
# Design: Gabrael Levine (G-Levine); source and modifications in root NOTICE.

"""Simple connected envelopes for bought hardware used by the simulation."""

import cadquery as cq

from machinome.node.cadquery import CadQueryNode
from machinome.motion.joints import Revolute


class CrossRollerOuterRace(CadQueryNode):
    """Fixed RA8008 outer envelope with 0.10 mm radial fit clearance."""

    color = "#727980"
    angular_deflection = 0.5

    def render(self):
        return cq.Workplane("XY").circle(47.9).circle(45.05).extrude(8.0)


class CrossRollerInnerRace(CadQueryNode):
    """Moving inner envelope with radial clearance from the printed carrier."""

    color = "#a7adb3"

    turn = Revolute(axis=(0, 0, 1), unit="deg")

    def render(self):
        return cq.Workplane("XY").circle(43.4).circle(40.1).extrude(8.0)


class PlanetBearing(CadQueryNode):
    """Connected 5 × 16 × 5 mm envelope for one 625ZZ bearing."""

    color = "#a7adb3"

    def render(self):
        return (
            cq.Workplane("XY")
            .circle(8.0)
            .circle(2.55)
            .extrude(5.0, both=True)
        )


class MotorStatorEnvelope(CadQueryNode):
    """Fixed 83 × 18 mm X8318 stator envelope named by the BOM alternate."""

    color = "#c9852c"

    def render(self):
        return cq.Workplane("XY").circle(41.5).extrude(18.0)


class MotorRotorEnvelope(CadQueryNode):
    """Rotating 92 × 22 mm Multistar can with a visible air gap."""

    color = "#d9a928"

    spin = Revolute(axis=(0, 0, 1), unit="deg")

    def render(self):
        return cq.Workplane("XY").circle(46.0).circle(41.7).extrude(22.0)


class EncoderBoardEnvelope(CadQueryNode):
    """22 × 28 mm AS5048 adapter-board envelope."""

    color = "#24734a"

    def render(self):
        return cq.Workplane("XY").rect(22.0, 28.0).extrude(1.6)
