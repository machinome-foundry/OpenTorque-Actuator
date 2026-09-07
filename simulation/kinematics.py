# SPDX-FileCopyrightText: 2026 Luis Henrique Cassis Fagundes
# SPDX-License-Identifier: AGPL-3.0-or-later
# Design: Gabrael Levine (G-Levine); source and modifications in root NOTICE.

"""Rigid fixed-ring planetary relations derived from source tooth counts."""

from .layout import PLANET_TEETH, REDUCTION, SUN_TEETH


def output_angle(input_angle):
    """Carrier/output angle for the fixed 126-tooth ring."""

    return input_angle / REDUCTION


def planet_relative_angle(input_angle):
    """Planet spin in its orbiting carrier frame."""

    return -(SUN_TEETH / PLANET_TEETH) * (input_angle - output_angle(input_angle))


def planet_absolute_angle(input_angle):
    """Planet orientation in the fixed actuator frame."""

    return output_angle(input_angle) + planet_relative_angle(input_angle)
