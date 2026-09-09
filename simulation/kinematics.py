# SPDX-FileCopyrightText: 2026 Luis Henrique Cassis Fagundes
# SPDX-License-Identifier: AGPL-3.0-or-later
# Design: Gabrael Levine (G-Levine); source and modifications in root NOTICE.

"""Rigid fixed-ring planetary relations derived from source tooth counts."""

from .layout import CARRIER_RATIO, SUN_PLANET_MESH


def output_angle(input_angle):
    """Carrier/output angle for the fixed 126-tooth ring."""

    return input_angle * CARRIER_RATIO


def planet_relative_angle(input_angle):
    """Planet spin in its orbiting carrier frame."""

    return SUN_PLANET_MESH * (input_angle - output_angle(input_angle))


def planet_absolute_angle(input_angle):
    """Planet orientation in the fixed actuator frame."""

    return output_angle(input_angle) + planet_relative_angle(input_angle)
