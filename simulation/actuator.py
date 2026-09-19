# SPDX-FileCopyrightText: 2026 Luis Henrique Cassis Fagundes
# SPDX-License-Identifier: CC-BY-SA-4.0
# Design: Gabrael Levine (G-Levine); source and modifications in root NOTICE.

"""Top-level OpenTorque actuator simulation."""

from machinome.node import AssemblyNode
from machinome.simulation import Driver, Instruction

from .hardware import EncoderBoardEnvelope, MotorRotorEnvelope, MotorStatorEnvelope
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
    # directly, and to the output carrier through the fixed-ring reduction,
    # sourced from the coordinate the reducer's OWN relations already
    # compute rather than restated from CARRIER_RATIO a second time.
    #
    # Task 9.6 of machinome's whole-tree-fixpoint cycle (ADR-099) asked
    # for exactly this sentence and this project's own
    # restate-reducer-chain-per-adr-099 change tried and reverted it: on a
    # freshly built instance it resolved correctly (`reducer.planet_1.orbit`
    # starts unbound, so the pass defers it, per ADR-099's own contract),
    # but on every SUBSEQUENT `set_state` against the SAME instance
    # `attempt(Root)` read a STALE value left over from the previous pass,
    # because `PlanetaryReducer` (the assembly whose phase clears and
    # recomputes that coordinate) had not run yet this pass -- measured at
    # maximum deviation 4.320e+02 over the project's 7 poses. That was a
    # framework defect, not a project limit: fixed upstream by
    # machinome's deferred-read-is-current change (archived
    # machinome/openspec/changes/archive/2026-09-11-deferred-read-is-current/),
    # which has `ResolvedEnd.bound()` recognize a value bound by the
    # attempting assembly or one of its own descendants during a PREVIOUS
    # pass as unready, so this attempt defers to the tree-wide fixpoint
    # instead of reading it early. Restated here now that the fix is
    # current; see this change's own repose probe.
    motor_rotor.spin.drives(reducer.sun_gear.spin)
    reducer.planet_1.orbit.drives(output_stack.planet_carrier_b.turn)

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
