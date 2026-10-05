# SPDX-FileCopyrightText: 2026 Luis Henrique Cassis Fagundes
# SPDX-License-Identifier: AGPL-3.0-or-later
# Design: Gabrael Levine (G-Levine); source and modifications in root NOTICE.

"""Exact parts selected from the upstream assembled STEP document."""

from machinome.node.step import StepNode
from machinome.motion.joints import Revolute

from .layout import GEAR_GROUP_Z, PLANET_GEAR_Z, PLANET_RADIUS


class ActuatorHousing(StepNode):
    """Printed housing carrying the reducer's fixed internal ring."""

    step_source = "../STEP/opentorque.step"
    part = "Actuator Housing"
    color = "#303238"
    angular_deflection = 0.5


class BearingRetainer(StepNode):
    """Printed retainer at the output face."""

    step_source = "../STEP/opentorque.step"
    part = "Bearing Retainer"
    color = "#303238"
    angular_deflection = 0.5


class PlanetCarrierA(StepNode):
    """Output-side printed carrier plate."""

    step_source = "../STEP/opentorque.step"
    part = "Planet Carrier A"
    color = "#d8d2bf"
    angular_deflection = 0.5

    turn = Revolute(axis=(0, 0, 1), unit="deg")


class PlanetCarrierB(StepNode):
    """Main printed planet carrier."""

    step_source = "../STEP/opentorque.step"
    part = "Planet Carrier B"
    color = "#d8d2bf"
    angular_deflection = 0.5

    turn = Revolute(axis=(0, 0, 1), unit="deg")


class PlanetCarrierC(StepNode):
    """Input-side printed carrier plate."""

    step_source = "../STEP/opentorque.step"
    part = "Planet Carrier C"
    color = "#d8d2bf"
    angular_deflection = 0.5

    turn = Revolute(axis=(0, 0, 1), unit="deg")


class Backplate(StepNode):
    """Printed motor-side backplate."""

    step_source = "../STEP/opentorque.step"
    part = "Backplate"
    color = "#303238"
    angular_deflection = 0.5


class EncoderCover(StepNode):
    """Printed encoder cover."""

    step_source = "../STEP/opentorque.step"
    part = "Encoder Cover"
    color = "#303238"
    angular_deflection = 0.5


class EncoderMagnetHolder(StepNode):
    """Printed rotating encoder magnet holder."""

    step_source = "../STEP/opentorque.step"
    part = "Encoder Magnet Holder"
    color = "#d8d2bf"
    angular_deflection = 0.5

    turn = Revolute(axis=(0, 0, 1), unit="deg")


class CrossRollerBearingSource(StepNode):
    """Source CAD for the RA-8008C bearing; retained for measurement."""

    step_source = "../STEP/opentorque.step"
    part = "RA-8008C Cross Roller Bearing"
    color = "#a7adb3"
    angular_deflection = 0.5


class SunGear(StepNode):
    """Standard 18-tooth herringbone sun selected from the assembly."""

    step_source = "../STEP/opentorque.step"
    part = "Sun Gear"
    color = "#eee8d5"
    angular_deflection = 0.5

    spin = Revolute(axis=(0, 0, 1), unit="deg")


class PlanetGear(StepNode):
    """Standard 54-tooth herringbone planet selected from the assembly."""

    step_source = "../STEP/opentorque.step"
    part = "Planet Gear"
    color = "#eee8d5"
    angular_deflection = 0.5

    spin = Revolute(axis=(0, 0, 1), unit="deg")


class PlanetBearingSource(StepNode):
    """Source CAD for one F625ZZ bearing; retained for measurement."""

    step_source = "../STEP/opentorque.step"
    part = "F625ZZ"
    color = "#a7adb3"
    angular_deflection = 0.5


class PlanetPin(StepNode):
    """Source M5x30 steel dowel pin."""

    step_source = "../STEP/opentorque.step"
    part = "M5x30 Dowel Pin"
    color = "#8d949a"
    angular_deflection = 0.5
