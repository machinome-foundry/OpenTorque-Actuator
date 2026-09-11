# SPDX-FileCopyrightText: 2026 Luis Henrique Cassis Fagundes
# SPDX-License-Identifier: CC-BY-SA-4.0
# Design: Gabrael Levine (G-Levine); source and modifications in root NOTICE.

"""Top-level OpenTorque actuator simulation."""

from solid_node.node import AssemblyNode
from solid_node.simulation import Driver, Instruction

from .hardware import EncoderBoardEnvelope, MotorRotorEnvelope, MotorStatorEnvelope
from .layout import CARRIER_RATIO
from .output_stack import OutputStack
from .reducer import PlanetaryReducer


class OpenTorqueActuator(AssemblyNode):
    """Complete rigid OpenTorque actuator driven by motor input angle."""

    input_angle = Driver(default=0.0, range=(-2880.0, 2880.0), unit="deg")

    instructions = {
        "Home": Instruction({"input_angle": 0.0}, duration=8.0),
        "One Motor Turn": Instruction({"input_angle": 360.0}, duration=1.0),
        "One Output Turn": Instruction({"input_angle": 2880.0}, duration=8.0),
    }

    output_stack = OutputStack()
    reducer = PlanetaryReducer()
    motor_stator = MotorStatorEnvelope()
    motor_rotor = MotorRotorEnvelope()
    encoder_board = EncoderBoardEnvelope()

    # The rotor's spin IS the machine's drive coordinate: keyed to the sun
    # directly, and to the output carrier through the fixed-ring reduction.
    #
    # Task 9.6 of solid-node's whole-tree-fixpoint cycle (ADR-099) asked
    # this line to be restated as `reducer.planet_1.orbit.drives(
    # output_stack.planet_carrier_b.turn)`, sourcing the carrier motion
    # from the coordinate the reducer's OWN relations already compute,
    # so CARRIER_RATIO is written once instead of twice. Tried and
    # reverted (evidence: openspec/changes/restate-reducer-chain-per-adr-099/
    # proposal.md): on a freshly built instance the sentence resolves
    # correctly, because `reducer.planet_1.orbit` starts unbound and the
    # pass defers it properly (ADR-099's own contract). On every
    # SUBSEQUENT `set_state` against the SAME instance it reads a STALE
    # value instead: `attempt(Root)` (root's own relations, resolved
    # before any child's phase runs) finds `reducer.planet_1.orbit`
    # already non-None -- the value it was left holding at the end of
    # the PREVIOUS pass, because `PlanetaryReducer` (the assembly whose
    # phase would clear and recompute it this pass) has not run yet --
    # and binds `output_stack.planet_carrier_b.turn` from it immediately
    # instead of deferring to the tree-wide fixpoint that would see the
    # fresh number. Measured directly against `capture_poses.py`'s own
    # repeated-pose sequence on one instance: maximum deviation 4.320e+02
    # over the project's 7 poses (`output_stack.*` bodies land on the
    # PREVIOUS pose's carrier angle, not the current one). The ratio is
    # therefore still stated twice, once here and once in the reducer,
    # both reading `CARRIER_RATIO` from `layout.py` so the two numbers
    # cannot drift, exactly as `move-onto-motion`'s Known gaps left it.
    motor_rotor.spin.drives(reducer.sun_gear.spin)
    motor_rotor.spin.drives(output_stack.planet_carrier_b.turn, ratio=CARRIER_RATIO)

    def render(self):
        # The 22 mm can ends at the source sun's Z=35 mm rear face.
        self.motor_rotor.translate((0.0, 0.0, 13.0))
        # The 18 mm stator shares that front face inside the can.
        self.motor_stator.translate((0.0, 0.0, 17.0 - 0.05))
        # The source cover admits the 22 × 28 mm PCB at Y=6 mm; its front
        # face remains 0.05 mm behind the magnet holder's source bound.
        self.encoder_board.translate((0.0, 6.0, -15.65))

    def simulate(self):
        self.motor_rotor.spin = self.input_angle


class ActuatorPosePreview(OpenTorqueActuator):
    """Snapshot-only preview: one motor turn from ``time=0`` to ``time=1``."""

    def simulate(self):
        self.motor_rotor.spin = self.input_angle + 360.0 * self.time
